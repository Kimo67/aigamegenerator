from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    hexcolor = models.CharField(max_length=32,blank=True, null=True)
    imagepath = models.CharField(max_length=512, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name