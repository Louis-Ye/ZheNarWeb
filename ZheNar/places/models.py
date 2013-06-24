from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User
# Create your models here.
class Icon(models.Model):
	name = models.CharField(unique=True,max_length=255)
	
	def __unicode__(self):
		return self.name[:-4]
	
class PlaceType(models.Model):
	STATUS_SET = (
	(1,"Pending"),
	(2,"Accepted"),
	(3,"Rejected"),
	)
	status = models.SmallIntegerField(default = 1,choices = STATUS_SET)
	name = models.CharField(max_length = 255,blank=False)
	icon = models.ForeignKey(Icon)
	#color: (optional) specifies a color either as a 24-bit (example: color=0xFFFFCC) 
	#or 32-bit hexadecimal value (example: color=0xFFFFCCFF), 
	#or from the set {black, brown, green, purple, yellow, blue, gray, orange, red, white}.


	def __unicode__(self):
		return self.name

class Place(models.Model):
	CHOICE_SET = (
	(1,"Pending"),
	(2,"Accepted"),
	(3,"Rejected"),
	)
	ZOOM_SET = (
	(16,"Large Level"),
	(17,"Middle Level"),
	(18,"Bottom Level"),
	)

	status = models.SmallIntegerField(default = 1,choices = CHOICE_SET)
	name = models.CharField(max_length = 255)
	creater = models.ForeignKey(User)
	description = models.TextField(blank = True)
	place_type = models.ForeignKey(PlaceType)
	latitude = models.FloatField()
	longitude = models.FloatField()
	create_time = models.DateField()
	zoom_level = models.SmallIntegerField(default = 18,choices = ZOOM_SET)
	
	def __unicode__(self):
		return self.name

	def showStatus(self):
		if self.status == 1: return "Pending"
		if self.status == 2: return "Accepted"
		if self.status == 3: return "Rejected"

	class Meta:
		ordering = ['name']
		permissions = (
			('create_map_place', 'Can create map place'),
			('modify_map_place', 'Can modify map place'),
			('remove_map_place', 'Can remove map place'),
		)
