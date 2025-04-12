from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.character import CharacterViewSet
from .views.case import CaseViewSet
from .views.story import StoryViewSet
from .views.charactercase import CharacterCaseViewSet

router = DefaultRouter()
router.register(r'characters', CharacterViewSet)  # This maps to /api/characters/
router.register(r'case', CaseViewSet)  # This maps to /api/case/
router.register(r'stories', StoryViewSet)
router.register(r'charactercase', CharacterCaseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]