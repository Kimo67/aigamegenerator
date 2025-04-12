from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import CharacterCase
from ..serializers import CharacterCaseSerializer

class CharacterCaseViewSet(viewsets.ModelViewSet):
    queryset = CharacterCase.objects.all()
    serializer_class = CharacterCaseSerializer
