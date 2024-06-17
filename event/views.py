"""
views for events
"""
from rest_framework.permissions import AllowAny
from event.models import Events
from rest_framework import viewsets
from event.serializers import EditEventSerializer,  JoinEventsSerializer
from account.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework import status
from event.permissions import UpdateOwnObjects
from django.http import HttpResponseRedirect


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


class ListAllEvents(viewsets.ModelViewSet):
    """listing all events"""
    serializer_class = JoinEventsSerializer
    queryset = Events.objects.all()
    permission_classes = [AllowAny, ]

    def list(self, request, *args, **kwargs):
        """list all the events"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(queryset.values())

    def create(self, request, *args, **kwargs):
        """creating event with user to be provider"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_name = serializer.data['course_name']
        course_id = Events.objects.filter(course_name=course_name).first().id
        return HttpResponseRedirect(redirect_to=f'http://127.0.0.1:8000/participant/joining/{course_id}')




