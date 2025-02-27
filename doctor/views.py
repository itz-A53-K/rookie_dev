from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from user.models import *
from datetime import datetime

# Create your views here.

@login_required(login_url='login')
def home(request):
    appointments = Appointment.objects.filter(doctor=request.user.id, status = "confirmed",  appointment_date = datetime.date.today())
    return render(request, 'doct/home.html', {'appointments': appointments})


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        doct = Doctor.objects.filter(email=email, password=password).first()

        if doct is not None:
            login(request, doct)
            return redirect('doct_home')
        else:
            return JsonResponse({'error': 'Invalid credentials'})
        
    return render(request, 'user/login.html')



@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def appointmentView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        appointment = Appointment.objects.get(id=id)

        return render(request, 'doct/appointment.html', {'appointment': appointment})


@login_required(login_url='login')
def addPrescription(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        prescription = request.FILES.get('prescription')

        appointment = Appointment.objects.get(id=id)
        appointment.prescription = prescription
        appointment.status = 'completed'
        appointment.save()

        return redirect('home')