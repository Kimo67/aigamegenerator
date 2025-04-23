# story/serializers/case.py
from rest_framework import serializers
from ..models.case import Case

class CaseSerializer(serializers.ModelSerializer):

    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Case
        fields = '__all__'  # Include all fields in the model (or specify the fields you need)