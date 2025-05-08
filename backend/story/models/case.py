from django.db import models
from .story import Story

class Case(models.Model):
    title = models.CharField(max_length=255)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    characters = models.ManyToManyField('Character', through='story.CharacterCase', related_name='cases')
    description = models.TextField(blank=True, null=True)
    prompt = models.TextField(blank=True, null=False)
    repliques = models.JSONField(default=list, blank=True, null=True)
    background = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
