# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from django.core.urlresolvers import reverse

from profiles.models import Profile


def index(request):
	if request.user.is_authenticated():
		return HttpResponse("This is places index!")
	else:
		return HttpResponseRedirect(reverse('ZheNar.views.index'))
