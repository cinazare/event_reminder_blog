from django.contrib import admin
from event.models import Events, Participants
# Register your models here.


class ParticipantsInline(admin.TabularInline):
    """makes controlling the users tabular inline"""
    model = Participants
    extra = 1


class EventAdmin(admin.ModelAdmin):
    """admin for events"""
    list_display = [
        'id',
        'provider',
        'course_name'
    ]
    inlines = [ParticipantsInline]


admin.site.register(Events, EventAdmin)

