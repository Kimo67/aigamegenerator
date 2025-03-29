from rest_framework import viewsets
from story.models.character import Character
from story.serializers.character import CharacterSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer