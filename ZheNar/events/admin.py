from django.contrib import admin
from events.models import EventType, Event, Icon

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Icon)
