from django.template import Template, Context, loader, RequestContext
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import datetime

def login_proc(request):
	if request.user.is_authenticated():
		return {
			"authenticated":True, 
			"username":request.user,
			}
	else:
		return {}

def index(request):
	c = Context({"page_title": "ZheNar ^o^"})
	return render_to_response('ZheNar/index.html',c,context_instance = RequestContext(request,processors=[login_proc]))

    
