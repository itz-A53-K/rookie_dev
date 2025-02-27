from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from user.models import *

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, 'user/home.html')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password, is_superuser=True)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return JsonResponse({'error': 'Invalid credentials'})
        
    return render(request, 'user/login.html')

@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def addDoctor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        dp = request.FILES.get('dp')
        qualification = request.POST.get('qualification')
        year_Of_Experience = request.POST.get('experience')

        fees = request.POST.get('fees')
        speciality = request.POST.get('speciality')

        available_days = request.POST.get('available_days')
        available_from = request.POST.get('available_from')
        available_to = request.POST.get('available_to')

        patient_per_day = request.POST.get('patient_per_day')

        Doctor.objects.create(
            name=name,
            email=email,
            password=password,
            dob=dob,
            phone=phone,
            gender=gender,
            image=dp,
            qualification=qualification,
            experience=year_Of_Experience,
            fees=fees,
            specialization=speciality,
            available_days=available_days,
            available_from=available_from,
            available_to=available_to,
            patient_per_day=patient_per_day,
        )
        return redirect('add_doctor')
    return render(request, 'manager/add_doctor.html')

        
