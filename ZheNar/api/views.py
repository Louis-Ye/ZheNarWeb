# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from datetime import datetime
import json

from profiles.models import Profile
from places.models import Place, PlaceType
from events.models import Event, EventType
def index(request):
	return HttpResponse("index!")

## -------------------------- user ---------------------------------------------------------

def user(request):
	if request.user.is_authenticated():
		user_info = __get_user_info(request.uer)
		return HttpResponse(json.dumps(user_info), mimetype='application/json')
	else :
		return HttpResponse(json.dumps({"error_code": "NotLoggedIn", }), status=403)


@csrf_exempt
@require_POST
def user_reg(request):
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	name = request.POST.get('student_name')
	gender = request.POST.get('gender')
	registerTime = datetime.now()
	if not (username and email and password):
		return HttpResponse(json.dumps({"error_code": "Can not be empty!", }), status=400)
	
	try:
		upr = User.objects.get(username=username)	#check if there is duplicated username
	except User.DoesNotExist:
		upr = None
	if upr is not None:
		return HttpResponse(json.dumps({"error": "用户名已被占用", }))

	try:
		upr = User.objects.get(email=email)		#check if there is duplicated email
	except User.DoesNotExist:
		upr = None
	if upr is not None:	
		return HttpResponse(json.dumps({"error": "Email已被使用", }))

	try:
		validate_email(email)
	except ValidationError:
		return HttpResponse(json.dumps({"error": "Email格式不正确", }))
	
	upr = User.objects.create_user(username, email, password)
	pr = Profile(user=upr, name=name, gender=gender, registerTime=registerTime)
	pr.save()

	return HttpResponse(json.dumps({"id": upr.id, }))


@csrf_exempt
@require_POST
def user_login_username(request):
	username = request.POST['username']
	password = request.POST['password']

	upr = authenticate(username=username, password=password)
	if upr is None:
		return HttpResponse(json.dumps({"error": "Email或密码错误",}))
	if upr.is_active == 0 or upr.is_superuser == 1:
		return HttpResponse(json.dumps({"error": "账户已被注销",}))

	user_info = __get_user_info(upr)
	return HttpResponse(json.dumps(user_info), mimetype='application/json')


@csrf_exempt
@require_POST
def user_login_email(request):
	email = request.POST['email']
	password = request.POST['password']

	upr = authenticate(email=email, password=password)
	if upr is None:
		return HttpResponse(json.dumps({"error": "Email或密码错误",}))
	if upr.is_active == 0 or upr.is_superuser == 1:
		return HttpResponse(json.dumps({"error": "账户已被注销",}))

	user_info = __get_user_info(upr)
	return HttpResponse(json.dumps(user_info), mimetype='application/json')


@csrf_exempt
@require_POST
def user_edit(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({"error_code": "NotLoggedIn", }), status=403)
	else:
		upr = request.user
		if request.POST['student_name']:
			upr.name = request.POST['student_name']
		if request.POST['password']:
			upr.password = request.POST['password']
		if request.POST['gender']:
			pr = Profile.objects.get(user_id=upr.id)
			pr.gender = request.POST['gender']
			pr.save()
		upr.save()


@csrf_exempt
@require_POST
def user_logout(request):
	logout(request)
	return HttpResponse("0")


def user_deactive(request):
	upr = request.user
	upr.is_active = 0
	logout(request)
	return HttpResponse("0")
	

def __get_user_info(upr):
	pr = Profile.objects.get(user_id = upr.id)
	user_info  = {
			"id"		: upr.id, 
			"username"	: upr.username,
			"email"		: upr.email,
			"gender"	: pr.gender,
			"student_name"	: pr.name,
	}
	return user_info

#-------------------------------------------------------------------------------------##------------------------------ Places

@csrf_exempt
@require_GET
def place(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({"error_code": "用户尚未登录", }), status=403)
	else:
		try:
			place_list = Place.objects.filter(status = 2)
		except Place.DoesNotExist:
			return HttpResponse(json.dumps({"error": "地点列表为空", }))
		
		place_info = {}
		for item in place_list:
			place_info[item.id] = __get_place_info(item)
		
		return HttpResponse(json.dumps(place_info), mimetype='application/json')
			
def __get_place_info(item):
	place_info = {
		"name"			:	item.name,
		"description" 	:	item.description,
		"latitude"		:	item.latitude,
		"longitude"		:	item.longitude,
		"type"			:	item.place_type.name,
	}
	return place_info
	
	
@csrf_exempt
@require_GET			
def place_type(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({"error_code": "用户尚未登录", }), status=403)
	else:
		try:
			place_type_list = PlaceType.objects.filter(status = 2)
		except PlaceType.DoesNotExist:
			return HttpResponse(json.dumps({"error": "地点类型列表为空", }))
			
		place_type_info = []
		
		for item in place_type_list:
			place_type_info.append(__get_place_type_info(item))
			
		return HttpResponse(json.dumps(place_type_info), mimetype='application/json') 
		
def __get_place_type_info(item):
	place_type_info = {
		"id"			: item.id,
		"name"			: item.name,
	}
	return place_type_info
	
#-------------------------------------------------------------------------------------##------------------------------ Events

@csrf_exempt
@require_GET
def event(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({"error_code": "用户尚未登录", }), status=403)
	else:
		try:
			event_list_query = Event.objects.filter(status = 2)
			event_list = [event for event in event_list_query if not event.if_event_was_expired()]
		except Event.DoesNotExist:
			return HttpResponse(json.dumps({"error": "事件列表为空", }))

		event_info = []
		for item in event_list:
			event_info.append(__get_event_info(item))

		return HttpResponse(json.dumps(event_info), mimetype='application/json')

def __get_event_info(item):
	event_info = {
		"id"			:	item.id,
		"name"			:	item.name,
		"description" 	:	item.description,
		"host"			:	item.holder.name,
		"organization"	:	item.host_organization,
		"start_time"	:	item.start_time.isoformat(),
		"end_time"		:	item.end_time.isoformat(),
		"place_id"		:	item.place.id,
		"address"		:	item.address,
		"follower_count":	100,	#暂时木有，等待添加#item.count_follower()
		"type"			:	item.event_type.name,
	}
	return event_info

@csrf_exempt
@require_GET			
def event_type(request):
	if not request.user.is_authenticated():
		return HttpResponse(json.dumps({"error_code": "用户尚未登录", }), status=403)
	else:
		try:
			event_type_list = EventType.objects.filter(status = 2)
		except EventType.DoesNotExist:
			return HttpResponse(json.dumps({"error": "事件类型列表为空", }))

		event_type_info = []

		for item in event_type_list:
			event_type_info.append(__get_event_type_info(item))

		return HttpResponse(json.dumps(event_type_info), mimetype='application/json') 

def __get_event_type_info(item):
	event_type_info = {
		"id"			: item.id,
		"name"			: item.name,
	}
	return event_type_info

	