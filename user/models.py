from django.db import models
from user.manager import UserManager
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
import uuid


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.CharField(max_length=11)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    USERNAME_FIELD="email"
    REQUIRED_FIELDS= ['name']

    objects= UserManager()
    def __str__(self):
        return self.email
    


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    age = models.PositiveSmallIntegerField()
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')

    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True)

    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"



class Doctor(models.Model):

    DAYS_OF_WEEK = (
        ("Mon", ("Monday")),
        ("Tue", ("Tuesday")),
        ("Wed", ("Wednesday")),
        ("Thu", ("Thursday")),
        ("Fri", ("Friday")),
        ("Sat", ("Saturday")),
        ("Sun", ("Sunday")),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    image = models.ImageField(upload_to='doct_images/', null=True, blank=True)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveSmallIntegerField()

    specialization = models.ForeignKey("doctSpecialization", on_delete=models.CASCADE)
    fees = models.PositiveIntegerField()

    available_days = MultiSelectField(choices=DAYS_OF_WEEK, max_choices=7, max_length=60)
    available_from = models.TimeField()
    available_to = models.TimeField()

    patient_per_day = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
    

class doctSpecialization(models.Model):
    specialization = models.CharField(max_length=100)
    desc = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.specialization

    # SPECIALIZATION       SPECIALIZATION DESC

	# Endocrinologist	  :Diabetes and Thyroid Specialist
	# Dentist	           -
	# Pediatrician        :Child Specialist
	# Therapist	           -
	# Dermatologist       :Skin, Hair, Nails Specialist
	# Gynaecologist        -
	# Cardiologist        :Heart Disease Specialis
	# Orthopedist	       -
	# Audiologists        :Ear specialist
