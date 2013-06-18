from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^create$',views.create,name='create'),
	url(r'^_create$',views._create,name='_create'),
	url(r'^type_create$',views.type_create,name='type_create'),
	url(r'^_type_create$',views._type_create,name='_type_create'),
)
