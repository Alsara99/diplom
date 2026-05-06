from .models import Worker, Task
from django.db.models import Count, Q, Prefetch
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NecessaryTaskSerializer, WorkerSerializer, TaskSerializer


class WorkersListView(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class TasksListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BusyWorkersListAPIView(APIView):
    def get(self, request):
        workers = Worker.objects.annotate(
            active_tasks_count=Count(
                'tasks',
                filter=Q(tasks__state='active')
            )
        ).prefetch_related(
            Prefetch(
                'tasks',
                queryset=Task.objects.filter(state='active'),
                to_attr='active_tasks'
            )
        ).order_by('-active_tasks_count')

        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)


class NecessaryTasksListAPIView(APIView):
    def get(self, request):
        necessary_tasks = Task.objects.filter(
            ~Q(state='active'),
            children__state='active'
        ).distinct()

        workers = list(
            Worker.objects.annotate(
                active_tasks_count=Count(
                    'tasks',
                    filter=Q(tasks__state='active')
                )
            )
        )

        if not workers:
            return Response([])

        least_loaded_worker = min(
            workers,
            key=lambda w: w.active_tasks_count
        )
        min_load = least_loaded_worker.active_tasks_count

        result = []

        for task in necessary_tasks:
            chosen_worker = least_loaded_worker

            child_task = task.children.filter(state='active').select_related('worker').first()

            if child_task and child_task.worker:
                candidate = child_task.worker
                candidate_obj = next((w for w in workers if w.id == candidate.id), None)

                if candidate_obj and candidate_obj.active_tasks_count <= min_load + 2:
                    chosen_worker = candidate

            result.append({
                "task": task.name,
                "deadline": task.deadline,
                "worker": chosen_worker.name if chosen_worker else None
            })

        serializer = NecessaryTaskSerializer(result, many=True)
        return Response(serializer.data)
