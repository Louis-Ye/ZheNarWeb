from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User)
	studentid = models.CharField(max_length=10, unique=True, blank=True, null=True)
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

