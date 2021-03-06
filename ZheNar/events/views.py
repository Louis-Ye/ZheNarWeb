# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import Context, loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count
from django.views.decorators.http import require_POST, require_GET

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
	pr = Profile.objects.get(user_id = request.user.id)
	followed_event = pr.event_follower_set.filter(status=2)
	"""
	for event in event_list:
		follower_list = event.follower.all()
		for man in follower_list:
			if man == user:
				followed_event.append(event)
	"""
	c = {
			'page_title': "浙Nar儿的事件",
			'event_list': event_list,
			'followed_event_list': followed_event,
	}
	return render_to_response("events/event_index.html",c,context_instance = RequestContext(request,processors=[login_proc]))

def _follow(request):
	event_id = request.POST.get("clicked_id")
	m_event = Event.objects.get(pk = event_id)

	m_event.follower.add(Profile.objects.get(user_id = request.user.id))
	return HttpResponse(json.dumps({"status":"succeed", }))

def _unfollow(request):
	event_id = request.POST.get("clicked_id")
	m_event = Event.objects.get(pk = event_id)
	
	m_event.follower.remove(Profile.objects.get(user_id = request.user.id))
	return HttpResponse(json.dumps({"status":"succeed", }))

def detail(request,event_id):
	try:
		m_event = Event.objects.get(pk = event_id)
	except Event.DoesNotExist:
		return __goErrorPage(request, ['There is no such event', ])
	m_follower = m_event.follower.all()[0:5]
	 
	c = Context({"page_title": "浙Nar儿的事件详情",
	"event": m_event,
	"followers": m_follower,
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
	holder = Profile.objects.get(user_id = request.user.id)
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
		event = Event(name=name, description=description, holder=holder, host_organization=host_organization, start_time=start_time, end_time=end_time, place_id=place_id, event_type_id=event_type_id, address = address)
		event_pic = request.FILES.get('event_pic')
		if request.user.is_superuser: 
			event.status = 2
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


@require_POST
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
		if request.user.is_superuser: 
			m_type.status = 2
		m_type.save()
		return HttpResponseRedirect(reverse('events:index'))
	
	return HttpResponseRedirect(reverse('index'))


def _delete(request, e_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	event = Event.objects.get(pk = e_id)
	pr = Profile.objects.get(user_id = request.user.id)
	if event.holder_id == pr.id:
		event.status = 4
		event.save()
	return HttpResponseRedirect(reverse('profiles:manage'))


def edit(request, event_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	event = Event.objects.get(pk=event_id)
	pr = Profile.objects.get(user_id = request.user.id)
	if event.holder_id != pr.id:
		return HttpResponseRedirect(reverse("index"))

	place_list = Place.objects.filter(status = 2)
	event_type_list = EventType.objects.filter(status = 2)
	context = {
			'page_title': "创建事件喽",
			'place_list': place_list,
			'event_type_list': event_type_list,
			'event':event,
			'event_start_time': event.start_time.strftime("%m/%d/%Y %H:%M:%S"),
			'event_end_time': event.end_time.strftime("%m/%d/%Y %H:%M:%S"),
	}
	return render(request, "events/event_edit.html", __login_proc(request, context))

def _edit(request, event_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	event = Event.objects.get(pk=event_id)
	pr = Profile.objects.get(user_id = request.user.id)
	if event.holder_id != pr.id:
		return HttpResponseRedirect(reverse("index"))

	name = request.POST.get("name")
	description = request.POST.get("description")
	holder = Profile.objects.get(user_id = request.user.id)
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
		event.name = name
		event.description=description
		event.holder=holder
		event.host_organization=host_organization
		event.start_time=start_time
		event.end_time = end_time
		m_place = Place.objects.get(pk = place_id)
		event.place = m_place
		m_event_type = EventType.objects.get(pk = event_type_id)
		event.event_type = m_event_type
		event.address = address
		if request.user.is_superuser: 
			event.status = 2
		event_pic = request.FILES.get('event_pic')
		if event_pic is not None:
			event.pic_name = handle_uploaded_pic(event_pic, event.id)
		event.save()
	else:
		return __goErrorPage(request, ['Something wrong with your form', ])

	return HttpResponseRedirect(reverse("events:index"))


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


