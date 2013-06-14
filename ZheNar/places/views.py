# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import render

from profiles.models import Profile


def index(request):
	if request.user.is_authenticated():
		return HttpResponse("This is places index!")
	else:
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
	
	
def create(request):
	return render(request,'places/place_create.html')
	
def _create(request):
	return HttpResponse("This is places creat handling page!")