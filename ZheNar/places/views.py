# -*- coding: utf-8 -*-
from django.template import Template, Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from datetime import datetime
from places.models import PlaceType,Place
from profiles.models import Profile

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
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
	
	
def create(request):
	if request.user.is_authenticated():
		m_place_type = PlaceType.objects.all()
		c = Context({"page_title": "ZJU地点",
					"place_options":m_place_type,
					})
		return render_to_response('places/place_create.html',c,context_instance = RequestContext(request,processors=[login_proc]))
	else:
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
	
def _create(request):
	if request.POST:
		m_place_name = request.POST.get('place_name')
		m_place_type_name = request.POST.get('place_type')
		m_latitude = request.POST.get('latitude')
		m_longitude = request.POST.get('longitude') 
		m_description = request.POST.get('description')
	else:
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
	
	m_place_type = PlaceType.objects.get(name = m_place_type_name)
	place = Place(name = m_place_name,description = m_description, place_type = m_place_type,latitude = m_latitude, longitude = m_longitude,create_time = datetime.now())
	place.save()
		
	return HttpResponseRedirect(reverse('places:index'))
	
