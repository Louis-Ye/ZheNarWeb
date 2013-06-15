# -*- coding: utf-8 -*-
from django.template import Template, Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
#from django.contrib.gis.maps.google.gmap import GoogleMap
#from django.contrib.gis.maps.google.overlays import GMarker, GEvent
from places.models import Place
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
	c = Context({"page_title": "浙哪儿欢迎你~",
				 "places":place_list,})
	return render_to_response('ZheNar/index.html',c,context_instance = RequestContext(request,processors=[login_proc]))

    
