# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from datetime import datetime
import json

from profiles.models import Profile

def index(request):
	return HttpResponse("index!")

def place(request):
	return HttpResponse("place!")

def event(request):
	return HttpResponse("event!")


## -------------------------- user ---------------------------------------------------------

def user(request):
	if request.user.is_authenticated():
		user_info = __get_user_info(request.uer)
		return HttpResponse(json.dumps(user_info), mimetype='application/json')
	else :
		return HttpResponse(json.dumps({"error_code": "NotLoggedIn", }), status=403)


def user_reg(request):
	if request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		studentid = request.POST.get('student_id')
		name = request.POST.get('student_name')
		gender = request.POST.get('gender')
		registerTime = datetime.now()
	else:
		return HttpResponse(json.dumps({"error_code": "不是POST", }), status=400)
	
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
	pr = Profile(user=upr, studentid=studentid, name=name, gender=gender, registerTime=registerTime)
	pr.save()

	return HttpResponse(json.dumps({"id": upr.id, }))


def user_login_username(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
	else:
		return HttpResponse(json.dumps({"error_code": "不是POST", }), status=400)

	upr = authenticate(username=username, password=password)
	if upr is None:
		return HttpResponse(json.dumps({"error": "Email或密码错误",}))
	if upr.is_active == 0 or upr.is_superuser == 1:
		return HttpResponse(json.dumps({"error": "账户已被注销",}))

	user_info = __get_user_info(upr)
	return HttpResponse(json.dumps(user_info), mimetype='application/json')


def user_login_email(request):
	if request.POST:
		email = request.POST['email']
		password = request.POST['password']
	else:
		return HttpResponse(json.dumps({"error_code": "不是POST", }), status=400)

	upr = authenticate(email=email, password=password)
	if upr is None:
		return HttpResponse(json.dumps({"error": "Email或密码错误",}))
	if upr.is_active == 0 or upr.is_superuser == 1:
		return HttpResponse(json.dumps({"error": "账户已被注销",}))

	user_info = __get_user_info(upr)
	return HttpResponse(json.dumps(user_info), mimetype='application/json')


def user_logout(request):
	if not request.POST:
		return HttpResponse(json.dumps({"error_code": "不是POST", }), status=400)
	logout(request)
	return HttpResponse("0")
	

def __get_user_info(upr):
	pr = Profile.objects.get(user_id = upr.id)
	user_info  = {
			"id"		: upr.id, 
			"username"	: upr.username,
			"email"		: upr.email,
			"gender"	: pr.gender,
			"student_id" 	: pr.studentid,
			"student_name"	: pr.name,
	}

#-------------------------------------------------------------------------------------------------------------------
