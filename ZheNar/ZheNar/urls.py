from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'ZheNar.views.index'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('api.urls', namespace="api")),
	url(r'^profiles/', include('profiles.urls', namespace="profiles")),
	url(r'^events/', include('events.urls',namespace="events")),
	url(r'^places/', include('places.urls',namespace="places")),
	# url(r'^api/', include('api.urls',namespace="api")),
    # Examples:
    # url(r'^$', 'ZheNar.views.home', name='home'),
    # url(r'^ZheNar/', include('ZheNar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
