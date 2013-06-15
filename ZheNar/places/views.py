# -*- coding: utf-8 -*-
from django.template import Template, Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from datetime import datetime
from places.models import PlaceType,Place,Icon
from profiles.models import Profile
from django.core.exceptions import ObjectDoesNotExist


def login_proc(request):
	if request.user.is_authenticated():
		return {
			"authenticated":True, 
			"username":request.user,
			}
	else:
		return {}
	
def debug(request, info):
	return HttpResponse("debug information: " + info)

def index(request):
	if request.user.is_authenticated():
		place_list = Place.objects.all()
		c = Context({"page_title": "ZJU地点",
					 "places": place_list,
					 })
		return render_to_response('places/place_index.html',c,context_instance = RequestContext(request,processors=[login_proc]))
	else:
		return HttpResponseRedirect(reverse('index'))
	
	
def create(request):
	if request.user.is_authenticated():
		m_place_type = PlaceType.objects.all()
		c = Context({"page_title": "ZJU地点",
					"place_options":m_place_type,
					})
		return render_to_response('places/place_create.html',c,context_instance = RequestContext(request,processors=[login_proc]))
	else:
		return HttpResponseRedirect(reverse('index'))
	
def _create(request):
	if request.POST:
		m_place_name = request.POST.get('place_name')
		m_place_type_name = request.POST.get('place_type')
		m_latitude = request.POST.get('latitude')
		m_longitude = request.POST.get('longitude') 
		m_description = request.POST.get('description')
	else:
		return HttpResponseRedirect(reverse('index'))
	
	m_place_type = PlaceType.objects.get(name = m_place_type_name)
	place = Place(name = m_place_name,description = m_description, place_type = m_place_type,latitude = m_latitude, longitude = m_longitude,create_time = datetime.now())
	place.save()
		
	return HttpResponseRedirect(reverse('places:index'))
	
	
def type_create(request):
	if request.user.is_authenticated():
		type_icon_list = Icon.objects.all()
		c = Context({"page_title": "ZJU地点-创建地点类型",
				"icon_list":type_icon_list,
		})
		return render_to_response('places/place_type_create.html',c,context_instance = RequestContext(request,processors=[login_proc]))
	else:
		return HttpResponseRedirect(reverse('places:index'))
	
def _type_create(request):
	error_list = []
	if request.POST:
		m_type_name = request.POST.get("place_type")
		m_type_icon = request.POST.get("place_icon")
	else:
		return HttpResponseRedirect(reverse('places:index'))
		

	m_icon = Icon.objects.get(name = m_type_icon)
	m_place_type = PlaceType(name = m_type_name, icon = m_icon)
	m_place_type.save()
	return HttpResponseRedirect(reverse('places:index'))
	
""" 用于插入icon用，已插入则无需再用
def insert(request):
	list = []
	f = open('static/map_icon/icon_list.txt','r')
	for line in f:
		list += line.splitlines()
	for item in list:
		icon = Icon(name= item)
		icon.save()
	return HttpResponseRedirect(reverse('places:index'))
"""