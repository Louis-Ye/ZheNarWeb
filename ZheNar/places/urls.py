from django.conf.urls import patterns, url

from place import views

urlpatterns = patterns('',
	url(r'^$',place.index,name='index'),
)