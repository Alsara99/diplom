from django.db import models

class Worker(models.Model):
    name = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.state})"

class Task(models.Model):
    name = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    worker = models.ForeignKey(Worker, related_name='tasks', on_delete=models.CASCADE)
    deadline = models.DateTimeField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.state})"
