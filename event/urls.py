"""
endpoints for events
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event.views import EventsViewSet, ListAllEvents

router = DefaultRouter()
router.register('user', EventsViewSet)
router.register('show', ListAllEvents, basename='list')
urlpatterns = router.urls


