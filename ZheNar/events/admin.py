# -*- coding: utf-8 -*-
from django.contrib import admin
from events.models import EventType, Event, Icon

class EventAdmin(admin.ModelAdmin):
	list_display = ('name','description','status','end_time','holder','host_organization','if_event_was_expired')
	search_fields = ('name','host_organization')
	list_filter = ('end_time',)
	ordering = ('-end_time',)
	fields = ('description','event_type','status','holder',)
	actions = ['make_accepted','make_rejected']
	
	def make_rejected(self, request, queryset):
		queryset.update(status = '3')
	
	make_rejected.short_description = '拒绝选择的请求'
	
	def make_accepted(self, request, queryset):
		queryset.update(status = '2')
	
	make_accepted.short_description = '接受选择的请求'

class EventTypeAdmin(admin.ModelAdmin):
	list_display = ('name','icon','status',)
	search_fields = ('name','icon',)
	actions = ['make_accepted','make_rejected']
	
	def make_rejected(self, request, queryset):
		queryset.update(status = '3')
	
	make_rejected.short_description = '拒绝选择的请求'
	
	def make_accepted(self, request, queryset):
		queryset.update(status = '2')
	
	make_accepted.short_description = '接受选择的请求'
	

class IconAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


admin.site.register(Event,EventAdmin)
admin.site.register(EventType,EventTypeAdmin)
admin.site.register(Icon,IconAdmin)
