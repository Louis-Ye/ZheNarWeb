from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.
class Profile(models.Model):
	THEMES_SET = (
	(1,_("Default")),
	(2,_("Cerulean")),
	(3,_("Cosmo")),
	(4,_("Flatly")),
	(5,_("Journal")),
	(6,_("Readable")),
	(7,_("Simplex")),
	(8,_("United")),
	(9,_("Spacelab")),
	)
	user = models.OneToOneField(User)
	name = models.CharField(max_length=255, blank=True, null=True)
	GENDER_CHOICES = (
        	(1, _('Male')),
        	(2, _('Female')),
	)
	gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
	registerTime = models.DateTimeField(blank = True, null = True)
	theme = models.PositiveSmallIntegerField(_('theme'),choices = THEMES_SET,default=1)

	def __unicode__(self):
		return self.user.username
		
