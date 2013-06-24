# -*- coding: utf-8 -*-
from django.contrib import admin
from places.models import PlaceType, Place, Icon

class PlaceAdmin(admin.ModelAdmin):
	list_display = ('name','description','status','create_time','creater',)
	search_fields = ('name','creater',)
	list_filter = ('create_time',)
	ordering = ('-create_time',)
	
	actions = ['make_accepted','make_rejected','make_deleted']
	
	def make_deleted(self, request, queryset):
		queryset.update(status = '4')
	
	make_deleted.short_description = '删除选择的请求'
	
	def make_rejected(self, request, queryset):
		queryset.update(status = '3')
	
	make_rejected.short_description = '拒绝选择的请求'
	
	def make_accepted(self, request, queryset):
		queryset.update(status = '2')
	
	make_accepted.short_description = '接受选择的请求'

class PlaceTypeAdmin(admin.ModelAdmin):
	list_display = ('name','icon','status',)
	search_fields = ('name','icon',)
	
	actions = ['make_accepted','make_rejected']
	
	def make_deleted(self, request, queryset):
		queryset.update(status = '4')
	
	make_deleted.short_description = '删除选择的请求'
	
	def make_rejected(self, request, queryset):
		queryset.update(status = '3')
	
	make_rejected.short_description = '拒绝选择的请求'
	
	def make_accepted(self, request, queryset):
		queryset.update(status = '2')
	
	make_accepted.short_description = '接受选择的请求'
	
class IconAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	
admin.site.register(Place,PlaceAdmin)
admin.site.register(PlaceType,PlaceTypeAdmin)
admin.site.register(Icon,IconAdmin)

