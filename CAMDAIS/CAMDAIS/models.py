from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class institute(models.Model):
	name = models.CharField(max_length=150)
	status = models.IntegerField()

class systemAdmin(models.Model):
	institute = models.ForeignKey(institute, on_delete=models.CASCADE)
	author = author = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.IntegerField()

class student(models.Model):
	institute = models.ForeignKey(institute, on_delete=models.CASCADE)
	author = author = models.ForeignKey(User, on_delete=models.CASCADE)
	level = models.IntegerField()
	status = models.IntegerField()