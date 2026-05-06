from rest_framework import serializers
from .models import Worker, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "worker",
            "deadline",
            "state",
        ]


class WorkerSerializer(serializers.ModelSerializer):
    active_tasks = serializers.SerializerMethodField()
    active_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = [
            "id",
            "name",
            "state",
            "active_tasks",
            "active_tasks_count",
        ]

    def get_active_tasks(self, obj):
        return Task.objects.filter(worker=obj, state='active').values_list('id', flat=True)

    def get_active_tasks_count(self, obj):
        return Task.objects.filter(worker=obj, state='active').count()


class NecessaryTaskSerializer(serializers.Serializer):
    task = serializers.CharField()
    deadline = serializers.DateTimeField(allow_null=True)
    worker = serializers.CharField(allow_null=True)
