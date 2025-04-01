from django.urls import path, include
from rest_framework.routers import DefaultRouter
from story.views.character import CharacterViewSet
from story.views.case import CaseViewSet

router = DefaultRouter()
router.register(r'characters', CharacterViewSet)  # This maps to /api/characters/
router.register(r'case', CaseViewSet)  # This maps to /api/case/

urlpatterns = [
    path('api/', include(router.urls)),
]