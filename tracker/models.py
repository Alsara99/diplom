from django.db import models

class Worker(models.Model):
    name = models.CharField(blank=True, null=True)
    role = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Task(models.Model):
    class Status:
        ACTIVE = "ACTIVE"
        DONE = "DONE"
        WAITING = "WAITING"

    STATUS_CHOICES = [
        (Status.ACTIVE, "Active"),
        (Status.DONE, "Done"),
        (Status.WAITING, "Waiting"),
    ]
    name = models.CharField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    worker = models.ForeignKey(Worker, related_name='tasks', on_delete=models.CASCADE)
    deadline = models.DateTimeField(blank=True, null=True)
    state = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=Status.WAITING
    )

    def __str__(self):
        return f"{self.name} ({self.state})"
