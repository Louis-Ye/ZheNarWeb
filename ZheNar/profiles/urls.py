from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^_login/$', views.login, name='_login'),
	url(r'^_register/$', views.register, name='_register'),
)

