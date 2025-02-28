from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='doct_home'),
    path('login/', views.loginView, name='doct_login'),
    path('appointment_details/', views.appointmentDetails, name='appointment_details'),
    path('appointment/update/', views.addPrescription, name='doct_add_prescription'),
    
]
