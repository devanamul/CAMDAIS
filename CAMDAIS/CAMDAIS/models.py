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

class classes(models.Model):
	Level = models.IntegerField()
	Maths_Anxiety_symptoms = models.BooleanField(default=True)
	Past_Experience = models.BooleanField(default=True)
	Learning_Habit = models.BooleanField(default=True)
	IQ = models.BooleanField(default=True)
	Arithmetic = models.BooleanField(default=True)
	Geometry = models.BooleanField(default=True)
	Algebra = models.BooleanField(default=True)
	Numerical_skill = models.BooleanField(default=True)
	Working_Memory = models.BooleanField(default=True)

class test(models.Model):
	class_id =  models.ForeignKey(classes, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	question = models.CharField(max_length=150)
	rightAns = models.CharField(max_length=150)
	ans2 = models.CharField(max_length=150)
	ans3 = models.CharField(max_length=150)
	ans4 = models.CharField(max_length=150)
