from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

def home(request):
    return render(request, 'user/home.html')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return JsonResponse({'error': 'Invalid credentials'})
        
    return render(request, 'user/login.html')


@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect("home")
    

def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        user = User.objects.create_user(email=email, name=name, dob=dob, phone=phone, gender=gender)
        user.set_password(password)
        user.save()
        return redirect('user_login')
    return render(request, 'user/register.html')



@login_required(login_url='login')
def appointmentView(request):
    if request.method == 'POST':

        age = request.POST.get('age')
        doctorID = request.POST.get('doctor')
        appointmentDate = request.POST.get('appointmentDate')
        

        user = request.user
        doctor = Doctor.objects.get(id = doctorID)
        applicationCount = Appointment.objects.filter(doctor = doctor, appointment_date = appointmentDate).count()

        if applicationCount >= doctor.patient_per_day:
            return JsonResponse({'error': f'No available slots for {appointmentDate}'})
        
        #time = available_from + (applicationCount * 30 min)
        appointmentTime = doctor.available_from + (applicationCount * 30 * 60)

        Appointment.objects.create(
            user = user,
            age = age,
            doctor = doctor,
            appointment_date = appointmentDate,
            appointment_time = appointmentTime
        )
        return JsonResponse({'success': 'Appointment booked successfully'})
    
    return render(request, 'user/appointment.html')
