# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime

from profiles.models import Profile

"""
def index(request):
	return HttpResponse("Haha~ index~")
"""

def _login(request):
	account = request.POST['account']
	password = request.POST['password']

	upr = authenticate(username=account, password=password)
	if upr is None:
		upr = authenticate(email=account, password=password) #check if user logins with email

	if upr is None:
		return HttpResponseRedirect() #There is no such user
	else :
		if upr.is_active == 0:
			return HttpResponseRedirect() #This user has not been active
		if upr.is_superuser == 1:
			return HttpResponseRedirect() #Super user should not login in this page

	return HttpResponseRedirect(reverse('ZheNar.views.index'))

def _logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('ZheNar.views.index'))

def register(request):
	context = {'someKey': 'someValue'}
	return render(request, 'profiles/register.html', context)

def _register(request):
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email']
	studentid = request.POST['studentid']
	name = request.POST['name']
	gender = request.POST['gender']
	registerTime = datetime.now()

	upr = User.objects.get(username=username)	#check if there is duplicated username
	if upr is not None:
		return HttpResponseRedirect()

	upr = User.objects.get(email=email)		#check if there is duplicated email
	if upr is not None:	
		return HttpResponseRedirect()
	
	upr = User.objects.create_user(username, email, password)
	pr = Profile(user=upr, studentid=studentid, name=name, gender=gender, registerTime=registerTime)
	pr.save()

	return HttpResponseRedirect()

def settings(request):
	if request.user.is_authenticated():
		context = {'someKey': 'someValue'}
		render(request, "profiles/settings.html", context)
	else :
		HttpResponseRedirect(reverse('ZheNar.views.index'))

