from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^_register/$', views._register, name='_register'),
	url(r'^_login/$', views._login, name='_login'),
	url(r'^_logout/$', views._logout, name='_logout'),
)

