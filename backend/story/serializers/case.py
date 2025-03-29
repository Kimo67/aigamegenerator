# story/serializers/case.py

from rest_framework import serializers
from ..models.case import Case

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'  # Include all fields in the model (or specify the fields you need)