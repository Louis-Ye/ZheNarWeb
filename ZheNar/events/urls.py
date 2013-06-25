from django.conf.urls import patterns, url

from events import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^create/$',views.create,name='create'),
	url(r'^_create/$',views._create,name='_create'),
	url(r'^type_create/$',views.type_create,name='type_create'),
	url(r'^_type_create/$',views._type_create,name='_type_create'),
	url(r'^detail/(?P<event_id>\d+)/$',views.detail,name='detail'),
	url(r'^_follow/$',views._follow,name='_follow'),
	url(r'^_unfollow/$',views._unfollow,name='_unfollow'),
	url(r'^insert/$',views.insert,name="insert"), #insert the icon
	url(r'^_delete/(?P<e_id>\d+)/$', views._delete,name='_delete'),
	url(r'^edit/(?P<event_id>\d+)/$',views.edit,name='edit'),
	url(r'^_edit/(?P<event_id>\d+)/$',views._edit,name='_edit'),
)
