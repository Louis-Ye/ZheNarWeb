# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from datetime import datetime

from profiles.models import Profile

def index(request):
	return HttpResponse("Haha~ index~")

def _login(request):
	account = request.POST['account']
	password = request.POST['password']
	upr = User.objects.get(username=account)
	if (upr == null) upr = User.objects.get(email=account)

	return HttpResponseRedirect(reverse('ZheNar.views.index'))

def _logout(request)
	return HttpResponseRedirect()

def register(request)
	context = {'someKey': 'someB'}
	return render(request, 'profiles/register.html', context)

def _register(request):
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email']
	studentid = request.POST['studentid']
	name = request.POST['name']
	gender = request.POST['gender']
	registerTime = datetime.now()
	
	upr = User.objects.create_user(username, email, password)
	pr = Profile(user=upr, studentid=studentid, name=name, gender=gender, registerTime=registerTime)
	pr.save()

	return HttpResponseRedirect()
