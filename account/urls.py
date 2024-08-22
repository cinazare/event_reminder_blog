from django.urls import path, include
from account.views import ParticipantsJoin, LoginApiView, RefreshAPIView

app_name = 'account'

urlpatterns = [
    path('join/<int:pk>/', ParticipantsJoin.as_view(), name='join-events'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
]