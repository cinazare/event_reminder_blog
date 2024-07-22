"""
views for events
"""
from rest_framework.permissions import AllowAny
from event.models import Events, Participants
from rest_framework import viewsets
from event.serializers import EditEventSerializer
from account.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from event.permissions import UpdateOwnObjects
from event.serializers import EventParticipantsSerializer


class EventsViewSet(viewsets.ModelViewSet):
    """view-set for events functionality"""
    queryset = Events.objects.all()
    serializer_class = EditEventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UpdateOwnObjects,]

    def list(self, request, *args, **kwargs):
        """retrieve all events of this user"""
        queryset = self.filter_queryset(self.get_queryset().filter(provider=request.user.id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """creating event with user to be provider"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = {'provider': request.user}
        serializer.save(**payload)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListAllEvents(viewsets.ViewSet):
    """listing events"""
    permission_classes = [AllowAny]

    def list(self, request):
        """list"""
        queryset = Events.objects.all()
        serializer = EditEventSerializer(queryset, many=True)
        return Response(serializer.data)


class EventParticipantsViewSet(viewsets.ModelViewSet):
    """functionality on every event users"""
    queryset = Participants.objects.all()
    serializer_class = EventParticipantsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """list all participants for event"""

    def retrieve(self, request, pk=None, *args, **kwargs):
        """retrieve special participant"""

    def destroy(self, request, pk=None, *args, **kwargs):
        """deleting special participant"""

    def put(self, request, pk=None, *args, **kwargs):
        """updating special field of user"""




