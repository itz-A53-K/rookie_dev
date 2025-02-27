from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='doct_home'),
    path('login/', views.loginView, name='doct_login'),
    path('logout/', views.logoutView, name='doct_logout'),
    path('appointment/', views.appointmentView, name='doct_appointment'),
    path('appointment/update/', views.addPrescription, name='doct_add_prescription'),
    
]
