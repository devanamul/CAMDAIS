from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def home(request):
	return render(request, "CAMDAIS/home.html")

def dashboard(request):
	u = request.user
	return render(request, "CAMDAIS/dashboard.html", {"user": u})

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

def signout(request):
	logout(request)
	return redirect('homepage')