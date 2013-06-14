from django.contrib import admin
from events.models import EventType, Event

admin.site.register(Event)
admin.site.register(EventType)