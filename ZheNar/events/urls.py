from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^disp/$',views.display_meta,name='display_meta'),
)
