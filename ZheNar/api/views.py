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

def index(request):
	return HttpResponse("index!")

def place(request):
	return HttpResponse("place!")

def event(request):
	return HttpResponse("event!")

def user(request):
	return HttpResponse("user!")

def login_email(request):
	return HttpResponse("login email!")
