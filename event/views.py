"""
views for events
"""
from rest_framework.permissions import AllowAny
from event.models import Events, Participants
from rest_framework import viewsets
from event.serializers import EditEventSerializer
from account.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework import status, generics
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


class ListAllEvents(generics.ListAPIView):
    """listing events"""
    permission_classes = [AllowAny]
    queryset = Events.objects.all()
    serializer_class = EditEventSerializer

    def list(self, request, *args, **kwargs):
        """listing all users events"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListCreateParticipants(generics.ListAPIView, generics.CreateAPIView):
    """listing Participants"""
    permission_classes = [IsAuthenticated]
    queryset = Participants.objects.all()
    serializer_class = EventParticipantsSerializer
    authentication_classes = [JWTAuthentication]

    def list(self, request, event_id=None, *args, **kwargs):
        """listing all users events"""
        queryset = self.filter_queryset(self.get_queryset()).filter(event=event_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, event_id=None, *args, **kwargs):
        """creating new participants"""
        event = Events.objects.get(id=event_id)
        payload = {
            'event': event
        }
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**payload)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EditEventParticipants(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView
    ):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Participants.objects.all()
    serializer_class = EventParticipantsSerializer

    def get(self, request, pk=None, *args, **kwargs):
        return self.retrieve(request, pk, *args, **kwargs)

    def put(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk=None, *args, **kwargs)

    def delete(self, request, pk=None, *args, **kwargs):
        return self.destroy(request, pk=None, *args, **kwargs)





