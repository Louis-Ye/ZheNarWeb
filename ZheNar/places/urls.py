from django.conf.urls import patterns, url

from places import views

urlpatterns = patterns('',
	url(r'^$',views.index, name='index'),
	url(r'^create$', views.create,name='create'),
	url(r'^_create$', views._create,name='_create'),
	#url(r'^modify$',views.create,name='modify'),
	
)
