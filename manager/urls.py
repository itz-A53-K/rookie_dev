from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('login/', views.loginView, name='manager_login'),
    path('logout/', views.logoutView, name='manager_logout'),
    path('add_doctor/', views.addDoctor, name='add_doctor'),
]
