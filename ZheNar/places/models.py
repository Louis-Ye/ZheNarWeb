from django.db import models

# Create your models here.
class PlaceType(models.Model):
	name = models.CharField(max_length = 255)

	def __unicode__(self):
		return self.name

class Place(models.Model):
	name = models.CharField(max_length = 255)
	description = models.TextField(blank = True)
	place_type = models.ForeignKey(PlaceType)
	latitude = models.FloatField()
	longitude = models.FloatField()

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
