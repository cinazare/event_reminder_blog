"""
serializer for events apis
"""
from rest_framework import serializers
from event.models import Events


class EditEventSerializer(serializers.ModelSerializer):
    """serializer for events objects """
    class Meta:
        model = Events
        fields = (
            'id',
            'course_name',
            'teacher_name',
            'number_of_sessions',
            'date_of_holding',
            'description'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class JoinEventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = (
            'id',
            'course_name',
        )




