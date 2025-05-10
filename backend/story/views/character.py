from rest_framework import viewsets
from ..models.character import Character
from ..serializers.character import CharacterSerializer

class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    #queryset.delete()
    serializer_class = CharacterSerializer