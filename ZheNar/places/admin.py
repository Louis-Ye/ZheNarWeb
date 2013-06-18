from django.contrib import admin
from places.models import PlaceType, Place, Icon

class PlaceAdmin(admin.ModelAdmin):
	list_display = ('name','description','status','create_time','creater',)
	search_fields = ('name','creater',)
	list_filter = ('create_time',)
	ordering = ('-create_time',)
	fields = ('description','place_type','status','creater',)

class PlaceTypeAdmin(admin.ModelAdmin):
	list_display = ('name','icon','status',)
	search_fields = ('name','icon',)
	
class IconAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	
admin.site.register(Place,PlaceAdmin)
admin.site.register(PlaceType,PlaceTypeAdmin)
admin.site.register(Icon,IconAdmin)

