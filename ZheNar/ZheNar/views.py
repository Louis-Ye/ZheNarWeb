from django.template import Template, Context
from django.http import HttpResponse
import datetime

def under_construction(request):
    now = datetime.datetime.now()
    t = Template("<html><body><h1>The website is now under construction!!</h1>It is now {{ current_date }}.</body></html>")
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)
    
