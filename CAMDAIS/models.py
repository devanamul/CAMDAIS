from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class institute(models.Model):
	name = models.CharField(max_length=150)
	status = models.IntegerField()
	instituteType = models.CharField(max_length=15)

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

class currentInstituteTest(models.Model):
	institute = models.ForeignKey(institute, on_delete=models.CASCADE)
	class_id =  models.ForeignKey(classes, on_delete=models.CASCADE)
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()

class currentGeneralTest(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	class_id =  models.ForeignKey(classes, on_delete=models.CASCADE)
	startDate = models.DateTimeField()
	endDate = models.DateTimeField()

class history(models.Model):
	test_type = models.IntegerField()
	examiner = models.ForeignKey(User, related_name='examiner', on_delete=models.CASCADE)
	examinee = models.ForeignKey(User, related_name='examinee', on_delete=models.CASCADE)
	level = models.IntegerField()
	Maths_Anxiety_symptoms = models.CharField(max_length=250, null=True, default=None)
	Past_Experience = models.CharField(max_length=250, null=True, default=None)
	Learning_Habit = models.CharField(max_length=250, null=True, default=None)
	IQ = models.CharField(max_length=250, null=True, default=None)
	Arithmetic = models.CharField(max_length=250, null=True, default=None)
	Geometry = models.CharField(max_length=250, null=True, default=None)
	Algebra = models.CharField(max_length=250, null=True, default=None)
	Numerical_skill = models.CharField(max_length=250, null=True, default=None)
	Working_Memory = models.CharField(max_length=250, null=True, default=None)
	Diagnostic_Result = models.CharField(max_length=1000, null=True, default=None)