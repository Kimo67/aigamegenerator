from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models.story import Story
from ..serializers.story import StorySerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    #queryset.delete()

    def destroy(self, request, *args, **kwargs):
        story = self.get_object()
        story.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Story.objects.filter(date_deleted__isnull=True)