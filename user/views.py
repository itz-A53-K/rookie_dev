from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.core.serializers import serialize

from .models import *
from datetime import datetime
import requests, json

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

        isUserExist = User.objects.filter(email=email).exists()
        if isUserExist:
            return JsonResponse({'error': 'User already exists','status':409, 'msg': 'User already exists. Please Login!'})

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

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        age = request.POST.get('age')
        doctorID = request.POST.get('doctor')
        appointmentDate = request.POST.get('date')
        

        user = request.user
        doctor = Doctor.objects.get(id = doctorID)
        applicationCount = Appointment.objects.filter(doctor = doctor, appointment_date = appointmentDate).count()

        if applicationCount >= doctor.patient_per_day:
            return JsonResponse({'error': f'No available slots for {appointmentDate}', 'status': 400})
        
        #time = available_from + (applicationCount * 30 min)
        appointmentTime = doctor.available_from + (applicationCount * 30 * 60)

        Appointment.objects.create(
            user = user,
            age = age,
            doctor = doctor,
            appointment_date = appointmentDate,
            appointment_time = appointmentTime
        )
        user.name = name
        user.email = email
        user.phone = phone
        user.save()

        return JsonResponse({'success': 'Appointment booked successfully', 'status': 200, 'time': appointmentTime, 'redirectLink': '/appointment-success'}) 
    
    doctCategory = doctSpecialization.objects.all()
    return render(request, 'user/book_appointment.html', {'doctCategory': doctCategory})


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
        day_name = date_obj.strftime("%a") 

        doctors = Doctor.objects.filter(specialization__name = doctCategory, available_days__contains = day_name)
        doctors_list = list(doctors.values("id", "name", "specialization"))
        return JsonResponse({'doctors': doctors_list}, status = 200)


@login_required(login_url='user_login')
def appointmentSuccess(request):
    return render(request, 'user/appointment_success.html')


def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'user/doctors.html', {'doctors': doctors})

def chat(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')  # Get message from request

        if not msg:
            return JsonResponse({'error': 'No message provided', 'status': 400})

        url = "https://ce38-34-105-54-130.ngrok-free.app/predict"  # Fixed URL formatting

        headers = {
            "Content-Type": "application/json",  # Ensure JSON is sent
            "ngrok-skip-browser-warning": "abc"
        }

        payload = {"message": msg}  # Create JSON payload


        try:
            resp = requests.post(url, json=payload, headers=headers)

            print(resp)

            if resp.status_code == 200:
                return JsonResponse({'msg': resp.json(), "status": 200})  # Use .json() to parse response 
            else:
                return JsonResponse({'error': 'Failed to get response', 'status': resp.status_code})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e), 'status': 500})  # Handle request errors

    return JsonResponse({'error': 'Invalid request method', 'status': 405})