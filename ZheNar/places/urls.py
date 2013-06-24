# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from places import views

urlpatterns = patterns('',
	url(r'^$',views.index, name='index'),
	url(r'^_debug/$',views.debug, name='debug'),
	url(r'^create/$', views.create,name='create'),
	url(r'^_create/$', views._create,name='_create'),
	url(r'^detail/(?P<place_id>\d+)/$',views.detail,name='detail'),
	url(r'^type_create/$', views.type_create,name='type_create'),
	url(r'^_type_create/$', views._type_create,name='_type_create'),
	url(r'^insert/$',views.insert,name="insert"), #用于插入icon
	#url(r'^modify$',views.create,name='modify'),
	#url(r'^_delete/(?P<e_id>\d+)/$', views._delete,name='_delete'),

)
