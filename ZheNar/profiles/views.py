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
		return HttpResponseRedirect(reverse('profiles:debug', args=("There is no such user", ))) #There is no such user
	else :
		if upr.is_active == 0:					#This user has not been active
			return HttpResponseRedirect(reverse('profiles:debug', args=("This user has not been active", )))
		if upr.is_superuser == 1:				#Superuser should not login in this page
			return HttpResponseRedirect(reverse('profiles:debug', args=("Superuser shouldn't login in this page", )))
	
	login(request, upr)		#log in
	return HttpResponseRedirect(reverse('index'))


def _logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def register(request):
	context = {'page_title': "浙哪儿注册喽！", }
	return render(request, 'profiles/register.html', context)


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
		return HttpResponseRedirect(reverse('profiles:debug', args=("duplicated username !", )))

	try:
		upr = User.objects.get(email=email)		#check if there is duplicated email
	except User.DoesNotExist:
		upr = None
	if upr is not None:	
		return HttpResponseRedirect(reverse('profiles:debug', args=("duplicated email !", )))
	
	upr = User.objects.create_user(username, email, password)
	pr = Profile(user=upr, name=name, gender=gender, registerTime=registerTime)
	pr.save()

	return HttpResponseRedirect(reverse('profiles:debug', args=("Successfully register !", )))


def settings(request):
	if request.user.is_authenticated():
		context = {'someKey': 'someValue'}
		return render(request, "profiles/settings.html", context)
	else :
		return HttpResponseRedirect(reverse('index'))

