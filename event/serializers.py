"""
serializer for events apis
"""
from rest_framework import serializers
from event.models import Events
from event.models import Participants


class EditEventSerializer(serializers.ModelSerializer):
    """serializer for events objects """
    class Meta:
        model = Events
        fields = (
            'id',
            'provider',
            'course_name',
            'teacher_name',
            'number_of_sessions',
            'date_of_holding',
            'description'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'provider':{'read_only': True}
        }


class JoinOnAnEventSerializer(serializers.ModelSerializer):
    """serializing users information to join on events"""

    class Meta:
        model = Participants
        fields = [
            'phone_number',
            'full_name',
            'student_number'
        ]
        extra_kwargs = {
            'phone_number': {
                'max_length': 11,
                'min_length': 11
            }
        }








