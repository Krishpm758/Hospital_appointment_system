"""
URL configuration for hospital1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
from tkinter.font import names

from django.contrib import admin
from django.urls import path
from patients import views

app_name='patients'
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
path('register',views.Register.as_view(),name='register'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('services', views.Service.as_view(), name='service'),
    path('appointment',views.Appointment.as_view(),name='appointment'),
    path('show', views.ShowAppointment.as_view(), name='show'),
    path('cancel/<int:i>/', views.CancelAppointment.as_view(), name='cancel'),
    path('print/<int:i>/', views.PrintAppointment.as_view(), name='print'),
    path('payment_success', views.PaymentSuccess.as_view(), name='payment_success'),
]