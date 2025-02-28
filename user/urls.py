from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginView, name='user_login'), 
    path('logout/', views.logoutView, name='user_logout'),
    path('register/', views.registerView, name='user_register'),
    path('book-appointment/', views.bookAppointment, name='book_appointment'),
    path('appointment-history/', views.appointmentHistory, name='appointment_history'),
    path('getDoctors/', views.getDoctors, name='get_doctors'), 
    path('appointment-success/', views.appointmentSuccess, name='appointment_success'),
    path("doctors/", views.doctors, name="doctors"),
]
