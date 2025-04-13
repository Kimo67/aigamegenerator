from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import CharacterCase
from ..serializers.charactercase import CharacterCaseSerializer

class CharacterCaseViewSet(viewsets.ModelViewSet):
    queryset = CharacterCase.objects.all()
    serializer_class = CharacterCaseSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            raise ValidationError("This character is already linked to this case.")