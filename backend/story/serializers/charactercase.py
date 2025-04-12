from rest_framework import serializers
from story.models import CharacterCase

class CharacterCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterCase
        fields = '__all__'