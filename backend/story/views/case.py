# story/views/case.py

from rest_framework import viewsets
from ..models.case import Case
from ..serializers.case import CaseSerializer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()  # The queryset to fetch the cases
    serializer_class = CaseSerializer  # The serializer for the Case model