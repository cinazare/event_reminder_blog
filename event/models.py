"""
models for events
"""

from account.models import User
from django.db import models


class Events(models.Model):
    """create events table in database"""
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    course_name = models.CharField(max_length=255, unique=True)
    teacher_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    number_of_sessions = models.SmallIntegerField()
    date_of_holding = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """retrieving course_name and provider_name"""
        return f'{str(self.provider)} >> {self.course_name}'

    # def get_id(self, course_name):
    #     """getting id back with the course name"""
    #     event = self.objects.filter(course_name=course_name).first().id
    #     if not event:
    #         return 0
    #
    #     return event

    def duplicate(self, phone_number):
        """checking the phone number to avoid duplication"""
        participant = self.participants.filter(phone_number=phone_number)
        if participant:
            return True

        return False


class Participants(models.Model):
    """participants in the system"""
    phone_number = models.CharField(max_length=11)
    full_name = models.CharField(max_length=255)
    student_number = models.CharField(max_length=10)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='participants')






