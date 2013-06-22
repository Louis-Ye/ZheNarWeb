from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
	url(r'^$',				views.index, name='index'),
	url(r'^place/$',		views.place, name='place'),
	url(r'^place/type$',	views.place_type,name='place_type'),
	url(r'^event/$',		views.event, name='event'),
	url(r'^event/type$',	views.event_type ,name='event_type'),
	url(r'^user/$',			views.user, name='user'),
	url(r'^user/reg/$',		views.user_reg, name='user_reg'),
	url(r'^user/login/username/$',	views.user_login_username, name='user_login_username'),
	url(r'^user/login/email/$',	views.user_login_email, name='user_login_email'),
	url(r'^user/edit/$',		views.user_edit, name='user_edit'),
	url(r'^user/logout/$',		views.user_logout, name='user_logout'),
	url(r'^user/deactive/$',	views.user_deactive, name='user_deactive'),
)
