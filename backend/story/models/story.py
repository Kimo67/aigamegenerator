from django.db import models
from django.utils import timezone


class Story(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def soft_delete(self):
        self.date_deleted = timezone.now()
        self.save()
