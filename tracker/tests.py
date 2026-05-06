from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Worker, Task


class WorkerTests(APITestCase):
    def test_create_worker(self):
        url = '/api/tracker/worker/new/'
        data = {"name": "Иван Иванов", "state": "active"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Worker.objects.count(), 1)

    def test_get_workers(self):
        Worker.objects.create(name="Test", state="active")

        response = self.client.get('/api/tracker/workers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_worker(self):
        worker = Worker.objects.create(name="Old", state="active")

        response = self.client.put(
            f'/api/tracker/worker/{worker.id}/edit/',
            {"name": "New", "state": "active"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_worker(self):
        worker = Worker.objects.create(name="Test", state="active")

        response = self.client.delete(f'/api/tracker/worker/{worker.id}/delete/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaskTests(APITestCase):

    def test_create_task(self):
        worker = Worker.objects.create(name="Worker", state="active")

        data = {
            "name": "Task 1",
            "worker": worker.id,
            "state": "active"
        }

        response = self.client.post('/api/tracker/task/new/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)


class BusyWorkersTests(APITestCase):

    def test_busy_workers_sorted(self):
        w1 = Worker.objects.create(name="W1")
        w2 = Worker.objects.create(name="W2")

        Task.objects.create(name="T1", worker=w1, state="active")
        Task.objects.create(name="T2", worker=w1, state="active")
        Task.objects.create(name="T3", worker=w2, state="active")

        response = self.client.get('/api/tracker/busy_workers/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data[0]['active_tasks_count'] >= response.data[1]['active_tasks_count'])


class NecessaryTasksTests(APITestCase):

    def test_necessary_tasks_logic(self):
        worker = Worker.objects.create(name="Worker")

        parent = Task.objects.create(name="Parent", state="new", worker=worker)
        child = Task.objects.create(name="Child", state="active", worker=worker, parent=parent)

        response = self.client.get('/api/tracker/necessary_tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['task'], "Parent")
