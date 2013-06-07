from django.template import Template, Context, loader
from django.shortcuts import render
from django.http import HttpResponse
import datetime

def index(request):
	context = {"page_title": "ZheNar ^o^"}
	return render(request, 'ZheNar/index.html', context)

	"""
	now = datetime.datetime.now()
	t = Template("<html><body><h1>The website is now under construction!!</h1>It is now {{ current_date }}.</body></html>")
	html = t.render(Context({'current_date':now}))
	return HttpResponse(html)
	"""
    
