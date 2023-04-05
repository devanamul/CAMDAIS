from django.shortcuts import render

def home(request):
	return render(request, "CAMDAIS/home.html")

def signin(request):
	if request.method == 'GET':
		return render(request, 'CAMDAIS/login.html')