# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import Context, loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count

from datetime import datetime
from profiles.models import Profile
import time
import json

from events.models import Event, EventType, Icon
from places.models import Place

def login_proc(request):
	if request.user.is_authenticated():
		return {
			"authenticated":True, 
			"username":request.user,
			}
	else:
		return {}


def index(request):
	event_list_query = Event.objects.filter(status=2)
	event_list = [event for event in event_list_query if not event.if_event_was_expired()]
	user = Profile.objects.get(user_id = request.user.id)
	followed_event = []
	for event in event_list:
		follower_list = event.follower.all()
		for man in follower_list:
			if man == user:
				followed_event.append(event)

	c = {
			'page_title': "浙Nar儿的事件",
			'event_list': event_list,
			'followed_event_list': followed_event,
	}
	return render_to_response("events/event_index.html",c,context_instance = RequestContext(request,processors=[login_proc]))

def _follow(request):
	event_id = request.POST.get("clicked_id")
	m_event = Event.objects.get(pk = event_id)

	m_event.follower.add(Profile.objects.get(id = request.user.id))
	return HttpResponse(json.dumps({"status":"succeed", }))

def _unfollow(request):
	event_id = request.POST.get("clicked_id")
	m_event = Event.objects.get(pk = event_id)
	
	m_event.follower.remove(Profile.objects.get(id = request.user.id))
	return HttpResponse(json.dumps({"status":"succeed", }))

def detail(request,event_id):
	try:
		m_event = Event.objects.get(pk = event_id)
	except Event.DoesNotExist:
		return __goErrorPage(request, ['There is no such event', ])
	
	c = Context({"page_title": "浙Nar儿的事件详情",
	"event": m_event,
	})
	return render_to_response('events/event_detail.html',c,context_instance = RequestContext(request,processors=[login_proc]))

def create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	place_list = Place.objects.filter(status = 2)
	event_type_list = EventType.objects.filter(status = 2)
	c = {
			'page_title': "创建事件喽",
			'place_list': place_list,
			'event_type_list': event_type_list,
	}
	return render_to_response("events/event_create.html",c,context_instance = RequestContext(request,processors=[login_proc]))
	

def _create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	name = request.POST.get("name")
	description = request.POST.get("description")
	holder_id = request.user.id
	host_organization = request.POST.get("host_organization")
	start_time_string = request.POST.get("start_time")
	start_time = datetime.strptime(start_time_string,"%m/%d/%Y %H:%M:%S")
	end_time_string = request.POST.get("end_time")
	end_time = datetime.strptime(end_time_string,"%m/%d/%Y %H:%M:%S")
	place_id = request.POST.get("place_id")
	event_type_id = request.POST.get("event_type_id")
	address = request.POST.get("address")
	
	try:
		obj_place = Place.objects.get(pk=place_id, status = 2)
	except Place.DoesNotExist:
		return __goErrorPage(request, ['There is no such place', ])
	try:
		obj_place = EventType.objects.get(pk=event_type_id, status = 2)
	except EventType.DoesNotExist:
		return __goErrorPage(request, ['There is no such event type', ])
	
	form = {}
	if __judge_form(form):
		event = Event(name=name, description=description, holder_id=holder_id, host_organization=host_organization, start_time=start_time, end_time=end_time, place_id=place_id, event_type_id=event_type_id, address = address)
		event_pic = request.FILES.get('event_pic')
		event.save()
		if event_pic is not None:
			event.pic_name = handle_uploaded_pic(event_pic, event.id)
			event.save()
		
	else:
		return __goErrorPage(request, ['Something wrong with your form', ])

	return HttpResponseRedirect(reverse("events:index"))


def handle_uploaded_pic(f, _id):
    pic_name = "event_" + str(_id) + ".jpg"
    with open('static/image/event_pic/' + pic_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return pic_name


def type_create(request):
	if request.user.is_authenticated():
		type_icon_list = Icon.objects.all()
		c = {
				'page_title': "浙哪儿事件类型创建", 
				'icon_list': type_icon_list,
		}
		return render_to_response("events/event_type_create.html",c,context_instance = RequestContext(request,processors=[login_proc]))
	else :
		return HttpResponseRedirect(reverse('places:index'))


def _type_create(request):
	error_list = []
	if request.POST:
		m_type_name = request.POST.get("event_type")
		m_type_icon = request.POST.get("event_icon")
	else:
		return HttpResponseRedirect(reverse('events:index'))
		
	try:
		m_type = EventType.objects.get(name = m_type_name,status = 2)
	except EventType.DoesNotExist:
		m_icon = Icon.objects.get(name = m_type_icon)
		m_type = EventType(name = m_type_name, icon = m_icon)
		m_type.save()
		return HttpResponseRedirect(reverse('events:index'))
	
	return HttpResponseRedirect(reverse('index'))


def hot(request):
	sorted_events = Event.objects.annotate(num_follower = Count("follower")).order_by("-num_follower").filter(status=2);
	active_events = [event for event in sorted_events if not event.if_event_was_expired() ]
	hot_event_list = active_events[0:10]

	user = Profile.objects.get(user_id = request.user.id)
	followed_event = []
	for event in hot_event_list:
		follower_list = event.follower.all()
		for man in follower_list:
			if man == user:
				followed_event.append(event)
	context = {
			"page_title": "十大热点事件",
			"hot_event_list": hot_event_list,
			'followed_event_list': followed_event,
	}
	return render(request, "events/event_hot.html", __login_proc(request, context))


def __judge_form(form):
	return True


def __goErrorPage(request, error_list):
	return render(request, "error/error_popup.html", __login_proc(request, {'error_list': error_list}))


def __login_proc(request, lst):
	if request.user.is_authenticated():
		lst['authenticated'] = True;
		lst['username'] = request.user.username
		return lst
	return lst
	

# 用于插入icon&place_type用，已插入则无需再用
def insert(request):
	list = []
	f = open('static/map_icon/icons/icon_list.txt','r')
	for line in f:
		list += line.splitlines()
	for item in list:
		icon = Icon(name= item)
		icon.save()
	

	return HttpResponseRedirect(reverse('events:index'))



