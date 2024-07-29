"""
endpoints for events
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event.views import EventsViewSet, ListAllEvents, ListCreateParticipants, EditEventParticipants


router = DefaultRouter()
router.register('user', EventsViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('list', ListAllEvents.as_view(), name='list'),
    path('<int:event_id>/participants', ListCreateParticipants.as_view(), name='event-participants'),
    path('edit/particpant/<int:pk>', EditEventParticipants.as_view(), name='edit-events-participants')
]


