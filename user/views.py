from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.core.serializers import serialize

from .models import *
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, 'user/home.html')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': 'Login successful','status':200, "redirectLink":"/"} )
        else:
            return JsonResponse({'error': 'Invalid credentials','status':401})
        
    return render(request, 'user/login.html')


@login_required(login_url='user_login')
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

        try:
            user = User.objects.create(email=email, name=name, dob=dob, phone=phone, gender=gender)
            user.set_password(password)
            user.save()
            return JsonResponse({'success': 'Registration successful','status':200} )
        except Exception as e:
            return JsonResponse({'error': str(e),'status':401})
        
    return render(request, 'user/register.html')



@login_required(login_url='user_login')
def bookAppointment(request):
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
    
    doctCategory = doctSpecialization.objects.all()
    return render(request, 'user/appointment.html', {'doctCategory': doctCategory})


@login_required(login_url='login')
def appointmentHistory(request):
    appointments = Appointment.objects.filter(user = request.user)
    return render(request, 'user/view_appointment.html', {'appointments': appointments})


@login_required(login_url='user_login')
def getDoctors(request):
    if request.method == 'POST':
        
        doctCategory = request.POST.get('specialization')
        date = request.POST.get('date')
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convert string to date
        day_name = date_obj.strftime("%A") 

        doctors = Doctor.objects.filter(specialization__name = doctCategory, available_days__contains = day_name)
        doctors_list = list(doctors.values("id", "name", "specialization"))
        return JsonResponse({'doctors': doctors_list}, status = 200)
