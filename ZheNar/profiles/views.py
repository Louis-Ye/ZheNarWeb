# Create your views here.
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from profiles.models import Profile

def index(request)
	return HttpResponse("Haha~ index~")

def login(request)
	return HttpResponse("This is login!")

def register(request)
	return HttpResponse("This is register page!")
