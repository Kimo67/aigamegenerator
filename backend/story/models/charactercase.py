from django.db import models

class CharacterCase(models.Model):
    character = models.ForeignKey('Character', on_delete=models.CASCADE, related_name='appearances')
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='character_links')

    # Character's specific data
    emotion = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # Positioning in the scene
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)  

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.character.name} in {self.case.title}"
