# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from profiles.models import Profile

def index(request):
	return HttpResponse("Haha~ index~")

def login(request):
	account = request.POST['account'];
	password = request.POST['password'];
	pr = Profile.objects.get();

	return HttpResponseRedirect()

def logout(request)
	return HttpResponseRedirect()

def register(request):
	return HttpResponseRedirect()
