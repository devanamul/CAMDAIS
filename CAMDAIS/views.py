from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import institute, systemAdmin, student, classes, test, currentInstituteTest


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
def SuperUser(request):
	return render(request, "CAMDAIS/superUser.html")

def signout(request):
	logout(request)
	return redirect('homepage')