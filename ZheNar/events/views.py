# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime

from events.models import Event, EventType

def index(request):
	return HttpResponse("This is events index!")


def create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	context = {
			'page_title': "创建事件喽",
	}
	return render(request, "events/event_create.html", __login_proc(request, context))
	

def _create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("index"))
	name = request.POST.get("name")
	description = request.POST.get("description")
	holder = request.user.id
	host_organization = request.POST.get("host_organization")
	start_time = request.POST.get("start_time")
	end_time = request.POST.get("end_time")
	place = request.POST.get("place_id")
	event_type = request.POST.get("event_type_id")


def type_create(request):
	context = {
			'page_title': "浙哪儿事件类型创建", 
	}
	return render(request, "events/event_type_create.html", __login_proc(request, context))


def _type_create(request):
	return HttpResponse("_type_create")


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
	
