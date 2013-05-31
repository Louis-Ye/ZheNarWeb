from django.db import models
from profiles.models import Profile
from places.models import Place
 
# Create your models here.
class Event(models.Model):
	name = models.CharField(max_length = 255)
	description = models.TextField(blank = True)
	holder = models.ForeignKey(Profile)
	host_organization = models.CharField(max_length = 255, null = True)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	place = models.ManyToManyField(Place)
	event_type = models.ForeignKey(EventType,null = False)
	
	def __unicode__(self):
		return self.name
		
	def event_lasting_time(self):
		return endTime - startTime 
	
	
	class Meta:
		ordering = ['name']
		
class EventType(models.Model):
	name = models.CharField(max_length = 255)
	
	def __unicode__(self):
		return self.name