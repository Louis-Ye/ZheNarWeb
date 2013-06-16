# Create your views here.
# <-* encoding=utf8 *->
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime

from profiles.models import Profile

import re, random


def index(request):
	return HttpResponse("index!")


def debug(request, info):
	return HttpResponse("debug information: " + info)


def _login(request):
	if request.POST:
		account = request.POST['account']
		password = request.POST['password']
	else:
		return HttpResponseRedirect(reverse('index'))

	upr = authenticate(username=account, password=password)
	if upr is None:
		upr = authenticate(email=account, password=password) #check if user logins with email

	if upr is None:
		return render(request,"error/error_popup.html",__login_proc(request,{'error_list':{"Wrong account or password"}}))
	else :
		if upr.is_active == 0:					#This user has not been active
			return render(request,"error/error_popup.html",__login_proc(request,{'error_list':{"This user have been disactivated"}}))
		if upr.is_superuser == 1:				#Superuser should not login in this page
			return render(request,"error/error_popup.html",__login_proc(request,{'error_list':{"Superuse should not login in this page"}}))
	
	login(request, upr)		#log in
	return HttpResponseRedirect(reverse('index'))


def _logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def register(request):
	context = {'page_title': "浙哪儿注册喽！", }
	return render(request, 'profiles/register.html', __login_proc(request, context))


def _register(request):
	if request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		name = request.POST.get('name')
		gender = 0
		if request.POST.get('gender') == 1:
			gender = 1
		elif request.POST.get('gender') == 2:
			gender = 2
		registerTime = datetime.now()
	else:
		return HttpResponseRedirect(reverse('index'))
	
	
	#return HttpResponse(username + email)

	try:
		upr = User.objects.get(username=username)	#check if there is duplicated username
	except User.DoesNotExist:
		upr = None
	if upr is not None:
		return render(request, "error/error_popup.html", __login_proc(request, {'error_list': {"duplicated username"}}))

	try:
		upr = User.objects.get(email=email)		#check if there is duplicated email
	except User.DoesNotExist:
		upr = None
	if upr is not None:	
		return render(request, "error/error_popup.html", __login_proc(request, {'error_list': {"dupicated email!"}}))
	
	form = {}
	if __judge_form(form):
		upr = User.objects.create_user(username, email, password)
		pr = Profile(user=upr, name=name, gender=gender, registerTime=registerTime)
		pr.save()
		userpr = authenticate(username=username, password=password)
		login(request, userpr)
	else:
		return render(request, "error/error_popup.html", __login_proc(request, {'error_list': {"something wrong with your form"}}))
	
	return HttpResponseRedirect(reverse('index'));


def __judge_form(form):
	return True


def settings(request):
	if request.user.is_authenticated():
		context = {'page_title': '浙哪儿设置'}
		return render(request, "profiles/settings.html", context)
	else :
		return HttpResponseRedirect(reverse('index'))


def __login_proc(request, lst):
	if request.user.is_authenticated():
		lst['authenticated'] = True;
		lst['username'] = request.user.username
		return lst
	return lst


