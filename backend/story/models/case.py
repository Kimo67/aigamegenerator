from django.db import models

class Case(models.Model):
    title = models.CharField(max_length=255)
    characters = models.ManyToManyField('Character', through='story.CharacterCase', related_name='cases')
    description = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    background = models.TextField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title