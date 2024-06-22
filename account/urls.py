from django.urls import path, include
from account.views import ParticipantsJoin

urlpatterns = [
    path('join/<int:pk>/', ParticipantsJoin.as_view(), name='participant-join-on-events')
]