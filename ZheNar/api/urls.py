from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^user/$',views.user,name='user'),
	url(r'^user/login/email$',views.login_email,name='user'),
	url(r'^place/$',views.place,name='place'),
	url(r'^event/$',views.event,name='event'),
)
