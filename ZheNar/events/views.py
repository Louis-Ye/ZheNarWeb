# Create your views here.
from django.http import HttpResponse, Http404

def index(request):
	return HttpResponse("This is events index!")
