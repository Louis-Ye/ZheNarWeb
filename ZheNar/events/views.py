# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime

from events.models import Event, EventType, Icon
from places.models import Place

def index(request):
	event_list = Event.objects.filter(status=2)
	context = {
			'page_title': "浙Nar儿的事件",
			'event_list': event_list,
	}
	return render(request, "events/event_index.html", __login_proc(request, context))


def create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	place_list = Place.objects.filter(status = 2)
	event_type_list = EventType.objects.filter(status = 2)
	context = {
			'page_title': "创建事件喽",
			'place_list': place_list,
			'event_type_list': event_type_list,
	}
	return render(request, "events/event_create.html", __login_proc(request, context))
	

def _create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	name = request.POST.get("name")
	description = request.POST.get("description")
	holder_id = request.user.id
	host_organization = request.POST.get("host_organization")
	start_time = datetime.now()#request.POST.get("start_time")
	end_time = datetime.now() #request.POST.get("end_time")
	place_id = request.POST.get("place_id")
	event_type_id = request.POST.get("event_type_id")
	
	try:
		obj_place = Place.objects.get(pk=place_id, status = 2)
	except Place.DoesNotExist:
		return __goErrorPage(request, ['There is no such place', ])
	try:
		obj_place = EventType.objects.get(pk=event_type_id, status = 2)
	except EventType.DoesNotExist:
		return __goErrorPage(request, ['There is no such event type', ])
	
	form={}
	if __judge_form(form):
		event = Event(name=name, description=description, holder_id=holder_id, host_organization=host_organization, start_time=start_time, end_time=end_time, place_id=place_id, event_type_id=event_type_id)
		event.save()
	else:
		return __goErrorPage(request, ['Something wrong with your form', ])

	return HttpResponseRedirect(reverse("events:index"))


def type_create(request):
	if request.user.is_authenticated():
		type_icon_list = Icon.objects.all()
		context = {
				'page_title': "浙哪儿事件类型创建", 
				'icon_list': type_icon_list,
		}
		return render(request, "events/event_type_create.html", __login_proc(request, context))
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


def __login_proc(request, lst):
	if request.user.is_authenticated():
		lst['authenticated'] = True;
		lst['username'] = request.user.username
		return lst
	return lst


def __judge_form(form):
	return True


def __goErrorPage(request, error_list):
	return render(request, "error/error_popup.html", __login_proc(request, {'error_list': error_list}))
	

""" 用于插入icon用，已插入则无需再用
def insert(request):
	list = []
	f = open('static/map_icon/icons/icon_list.txt','r')
	for line in f:
		list += line.splitlines()
	for item in list:
		icon = Icon(name= item)
		icon.save()
	return HttpResponseRedirect(reverse('places:index'))
"""

