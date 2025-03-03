from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from user.models import *
from datetime import datetime, date

# Create your views here.

def home(request):
    if "doctor_id" not in request.session:
        return redirect("doct_login")
    appointments = Appointment.objects.filter(doctor= request.session["doctor_id"])
    return render(request, 'doct/home.html', {'appointments': appointments})


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        doct = Doctor.objects.filter(email=email, password=password).first()

        if doct is not None:
            request.session['doctor_id'] = doct.id 
            return JsonResponse({'success': 'Login successful','status':200, "redirectLink":"/doct/"} )
        else:
            return JsonResponse({'error': 'Invalid credentials','status':401})
        
    return render(request, 'user/login.html')



def appointmentDetails(request):
    if "doctor_id" not in request.session:
        return redirect("doct_login")
    
    id = request.GET.get('appointmentId')

    appointment = Appointment.objects.get(id=id)

    history = Appointment.objects.filter(user = appointment.user, status = "completed")

    return render(request, 'doct/appointment_details.html', {'appointment': appointment, "history": history})


@login_required(login_url='doct_login')
def addPrescription(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        prescription = request.FILES.get('prescription')

        appointment = Appointment.objects.get(id=id)
        appointment.prescription = prescription
        appointment.status = 'completed'
        appointment.save()

        return JsonResponse({'success': 'Prescription added successfully', "status": 200})