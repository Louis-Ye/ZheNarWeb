from django.conf.urls import patterns, url

from places import views

urlpatterns = patterns('',
	url(r'^$',views.index, name='index'),
	#url(r'^create$', views.create,name='create'),
	#url(r'^modify$',views.create,name='modify'),
	
)
