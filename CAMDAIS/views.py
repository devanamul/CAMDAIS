from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import institute, systemAdmin, student, classes, test, currentInstituteTest
from datetime import datetime, timedelta


def home(request):
	return render(request, "CAMDAIS/home.html")

def dashboard(request):
	userType = None;
	u = request.user
	is_admin = systemAdmin.objects.filter(author=u)
	is_student = student.objects.filter(author=u)
	my_institute = None
	if is_admin.exists():
		userType = 'admin'
		print(userType)
		is_admin = systemAdmin.objects.get(author=u)
		my_institute = institute.objects.get(id=is_admin.institute.id)
	elif is_student.exists():
		userType = 'student'
		is_student = student.objects.get(author=u)
		my_institute = institute.objects.get(id=is_student.institute.id)
	print(u.first_name, userType)
	return render(request, "CAMDAIS/dashboard.html", {"user": u, 'userType': userType, 'my_institute':  my_institute})

def signin(request):
	if request.method == 'GET':
		return render(request, 'CAMDAIS/login.html')
	elif request.method == 'POST' and 'login' in request.POST:
		u = request.POST.get('username')
		p = request.POST.get('pass')
		user = authenticate(username=u, password=p)
		if user is None:
			return render(request, 'CAMDAIS/login.html')
		else:
			login(request, user)
			return redirect('Dashboard')
	elif request.method == 'POST' and 'SignUp' in request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		password = request.POST.get('password')
		
		
		try:
			create_user = User.objects.create_user(
				username=username,
				email=email,
				first_name=first_name,
				last_name=last_name,
				password=password
				)
		except ValueError as e:
			error_message = str(e)
			return render(request, "CAMDAIS/login.html", {'error_message': error_message})
		
		create_user.save()
		messages.success(request, 'Successfully registered!')
		return redirect('SignIn')

def insttuteForm(request):
	if request.method == 'GET':
		return render(request, 'CAMDAIS/adminForm.html')
	elif request.method == 'POST':
		u = request.user
		name = request.POST.get('instituteName')
		instituteType = request.POST.get('InstituteType')
		current_institutes = institute.objects.filter(name = name)
		if current_institutes is  None:
			new_institute = institute(name=name, status = 0, instituteType=instituteType)
			new_institute.save()
			new_systemAdmin = systemAdmin(institute = new_institute, author = u, status = 0)
			new_systemAdmin.save()

			if new_institute.id and new_systemAdmin.id:
				print("Ok")
				return redirect('Dashboard')
			else:
				return render(request, 'CAMDAIS/adminForm.html', {'message': "something is wrong, try again"})
		else:
			return render(request, 'CAMDAIS/adminForm.html', {'message': "Institute already exists, Enter valid institute name"})

def studentForm(request):
	u = request.user
	current_institutes = institute.objects.all()
	if request.method == 'GET':
		return render(request, 'CAMDAIS/studentForm.html', {"institutes" : current_institutes})
	elif request.method == 'POST':
		institute_id = request.POST.get('Institute')
		level_str = request.POST.get('level')
		level = int(level_str)
		if 3 > level or level > 10:
			return render(request, 'CAMDAIS/studentForm.html', {"institutes" : current_institutes, 'message': "this class is not exist, please enter a valid class number (3-10)"})
		else:
			my_institute = institute.objects.get(id = institute_id)
			new_student = student(author = u, level = level, status = 0, institute = my_institute)
			new_student.save()

			if new_student.id:
				return redirect('Dashboard')
			else:
				return render(request, 'CAMDAIS/studentForm.html', {"institutes" : current_institutes, 'message': "something is wrong, try again"})

def insttutePage(request):
	if request.method == 'GET':
		userType = None;
		u = request.user
		is_admin = systemAdmin.objects.filter(author=u)
		is_student = student.objects.filter(author=u)
		my_institute = None
		if is_admin.exists():
			userType = 'admin'
			print(userType)
			is_admin = systemAdmin.objects.get(author=u)
			my_institute = institute.objects.get(id=is_admin.institute.id)
		elif is_student.exists():
			userType = 'student'
			is_student = student.objects.get(author=u)
			my_institute = institute.objects.get(id=is_student.institute.id)
		return render(request, 'CAMDAIS/institutePage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute})

def studentPage(request):
	if request.method == 'GET':
		userType = None;
		u = request.user
		is_admin = systemAdmin.objects.filter(author=u)
		is_student = student.objects.filter(author=u)
		my_institute = None
		if is_admin.exists():
			userType = 'admin'
			print(userType)
			is_admin = systemAdmin.objects.get(author=u)
			my_institute = institute.objects.get(id=is_admin.institute.id)
		elif is_student.exists():
			userType = 'student'
			is_student = student.objects.get(author=u)
			my_institute = institute.objects.get(id=is_student.institute.id)
		return render(request, 'CAMDAIS/studentPage.html', {"user": u, 'userType': userType, 'my_institute':  my_institute})

def makeTest(request):
	userType = None;
	u = request.user
	is_admin = systemAdmin.objects.filter(author=u)
	is_student = student.objects.filter(author=u)
	my_institute = None
	if is_admin.exists():
		userType = 'admin'
		is_admin = systemAdmin.objects.get(author=u)
		my_institute = institute.objects.get(id=is_admin.institute.id)
	elif is_student.exists():
		userType = 'student'
		is_student = student.objects.get(author=u)
		my_institute = institute.objects.get(id=is_student.institute.id)
	class_dict = {}
	for i in range(3, 11):
		key = "class " + str(i)
		# print(key)
		classN = classes.objects.get(Level=i)
		true_count = 0
		for each in ['Maths_Anxiety_symptoms', 'Past_Experience', 'Working_Memory', 'Numerical_skill', 'Algebra', 'Geometry', 'Arithmetic', 'Learning_Habit', 'IQ']:
			if getattr(classN, each):
				true_count += 1
		class_dict[f'class_{i}'] = {'level': i, 'test': true_count}
	if request.method == 'GET':
		
		# for key in class_dict:
		# 	current_class = class_dict[key]
		# 	print(current_class['level'] , " ",  current_class['test'])
		
		return render(request, 'CAMDAIS/makeTest.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'class_dict': class_dict})
	
	elif request.method == 'POST':
		# level_str = request.POST.get('level')
		level = request.POST.get('level')
		my_class = classes.objects.get(Level = level)
		instituteId = request.POST.get('instituteId')
		my_institute = institute.objects.get(id = instituteId)
		startDate = datetime.now()
		endDate = datetime.now() + timedelta(days=5)
		# print("start date ", startDate, " ", endDate)
		current_test = currentInstituteTest.objects.filter(institute = my_institute)
		print(current_test)
		if current_test.exists():
			return render(request, 'CAMDAIS/makeTest.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'class_dict': class_dict, 'message': "Already there is a running test for this class"})
		else:
			new_currentInstituteTest = currentInstituteTest(institute = my_institute, class_id = my_class, startDate = startDate, endDate = endDate)
			new_currentInstituteTest.save()
			if new_currentInstituteTest.id:
				return redirect('Dashboard')
			else:
				return render(request, 'CAMDAIS/makeTest.html', {"user": u, 'userType': userType, 'my_institute':  my_institute, 'class_dict': class_dict, 'message': "something is wrong, try again"})
			

def SuperUser(request):
	return render(request, "CAMDAIS/superUser.html")

def signout(request):
	logout(request)
	return redirect('homepage')