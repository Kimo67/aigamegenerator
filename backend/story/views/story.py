from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from ..models.story import Story
from ..serializers.story import StorySerializer
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def destroy(self, request, *args, **kwargs):
        story = self.get_object()
        story.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Story.objects.filter(date_deleted__isnull=True)
    
    @action(detail=False, methods=['get'], url_path='renpy')
    def custom_get(self, request):
        # Custom logic here (e.g. filtered queryset, stats, etc.)
        ai_response = requests.post(
            "http://ai-script-app:8050/story/add-node",
        )
        return Response(ai_response)