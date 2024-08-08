from django.urls import path, include
from account.views import ParticipantsJoin, LoginApiView

app_name = 'account'

urlpatterns = [
    path('join/<int:pk>/', ParticipantsJoin.as_view(), name='participant-join-on-events'),
    path('login/', LoginApiView.as_view(), name='login'),
]