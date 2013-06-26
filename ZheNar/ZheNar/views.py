# -*- coding: utf-8 -*-
from django.template import Template, Context, loader, RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Count
from django.core.urlresolvers import reverse
#from django.contrib.gis.maps.google.gmap import GoogleMap
#from django.contrib.gis.maps.google.overlays import GMarker, GEvent
from places.models import Place
from events.models import Event
from profiles.models import Profile
from django.contrib.auth.models import User
import datetime

def login_proc(request):
	if request.user.is_authenticated():
		return {
			"authenticated":True, 
			"username":request.user,
			}
	else:
		return {}

def index(request):
	place_list = Place.objects.filter(status = 2)
	event_list_query = Event.objects.filter(status = 2)
	event_list = [event for event in event_list_query if not event.if_event_was_expired()]
	c = Context({"page_title": "浙哪儿欢迎你~",
				 "places":place_list,
				 "events":event_list,})
	return render_to_response('ZheNar/index.html',c,context_instance = RequestContext(request,processors=[login_proc]))

    
def hot(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))

	sorted_events = Event.objects.annotate(num_follower = Count("follower")).order_by("-num_follower").filter(status=2);
	active_events = [event for event in sorted_events if not event.if_event_was_expired() ]
	hot_event_list = active_events[0:10]

	pr = Profile.objects.get(user_id = request.user.id)
	followed_event = pr.event_follower_set.filter(status=2)

	places = Place.objects.filter(status=2)
	for item in places: 
		item.syncEventsFollowers()
	pls = list(places)
	pls.sort()
	hot_place_list = pls[0:10]
	context = {
			"page_title": "十大热点",
			"hot_event_list": hot_event_list,
			"followed_event_list": followed_event,
			"hot_place_list": hot_place_list,
	}
	return render(request, "ZheNar/zhenar_hot.html", __login_proc(request, context))


def __login_proc(request, lst):
	if request.user.is_authenticated():
		lst['authenticated'] = True;
		lst['username'] = request.user.username
		return lst
	return lst

