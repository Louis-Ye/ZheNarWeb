from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^debug/(?P<info>[\S ]+)/$', views.debug, name='debug'),
	url(r'^_login/$', views._login, name='_login'),
	url(r'^_logout/$', views._logout, name='_logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^_register/$', views._register, name='_register'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^_settings/$', views._settings, name='_settings'),
	url(r'^syncSuperUser/$', views.syncSuperUser, name='syncSuperUser'),#for sync the superuser into profile
)

