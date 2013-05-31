#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User)
	studentid = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=255)

