from rest_framework import serializers
from ..models.character import Character  # Import the model

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'  # Specify the fields to serialize