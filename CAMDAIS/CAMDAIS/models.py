from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class institute(models.Model):
	name = models.CharField(max_length=150)
	status = models.IntegerField()
