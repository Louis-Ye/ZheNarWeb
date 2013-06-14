# -*- coding: utf-8 -*-
from django.template import Template, Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from profiles.models import Profile

def login_proc(request):
	if request.user.is_authenticated():
		return {
			"authenticated":True, 
			"username":request.user,
			}
	else:
		return {}
	
	

def index(request):
	if request.user.is_authenticated():
		c = Context({"page_title": "ZJU地点"})
		#通过使用render_to_response来将一些页面的必要信息加入模板中
		return render_to_response('places/place_index.html',c,context_instance = RequestContext(request,processors=[login_proc]))
	else:
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
	
	
def create(request):
	if request.user.is_authenticated():
		c = Context({"page_title": "ZJU地点"})
		return render_to_response('places/place_create.html',c,context_instance = RequestContext(request,processors=[login_proc]))
	else:
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
	
def _create(request):
	if request.POST:
		place_name = request.POST.get('place_name')
		place_type = request.POST.get('place_type') 
	return HttpResponse("This is places creat handling page!")
	
