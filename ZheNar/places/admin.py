from django.contrib import admin
from places.models import PlaceType, Place

class PlaceAdmin(admin.ModelAdmin):
	list_display = ('name','description','status','create_time')
	search_fields = ('name',)
	list_filter = ('create_time',)
	ordering = ('-create_time',)
	fields = ('description','place_type','status',)

admin.site.register(Place,PlaceAdmin)
admin.site.register(PlaceType)

