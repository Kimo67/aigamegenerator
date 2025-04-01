from rest_framework import serializers
from ..models.character import Character  # Import the model

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'age', 'description']  # Specify the fields to serialize