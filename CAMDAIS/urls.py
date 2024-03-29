"""CAMDAIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('signin/', views.signin, name='SignIn'),
    path('dashboard/', views.dashboard, name = 'Dashboard'),
    path('logout/', views.signout, name='Logout'),
    path('instituteForm/', views.insttuteForm, name='InsttuteForm'),
    path('studentForm/', views.studentForm, name='StudentForm'),
    path('institutePage/', views.insttutePage, name='InsttutePage'),
    path('studentPage/', views.studentPage, name='StudentPage'),
    path('makeTest/', views.makeTest, name='MakeTest'),
    path('testPage/', views.attempt, name='TestPage'),
    path('resultAppeared/', views.AppearedResult, name='ResultAppeared'),
    path('superuser/', views.SuperUser, name='SuperUser'),
    
] 