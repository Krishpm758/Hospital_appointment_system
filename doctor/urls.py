"""
URL configuration for hospital project.

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
from django.contrib import admin
from django.urls import path

from doctor import views
from doctor import views

app_name='doctor'
urlpatterns = [
    path('department',views.Departmentview.as_view(),name='dept'),
    path('doctor/<int:i>',views.DoctorView.as_view(),name='doc'),
    path('alldoc',views.Alldoctor.as_view(),name='alldoc'),
    path('singledoc/<int:i>',views.Singledoc.as_view(),name='singledoc'),
    path('adddept', views.AddDepartment.as_view(), name='adddept'),
    path('adddoc', views.AddDoctor.as_view(), name='adddoc'),
    path('edit/<int:i>',views.Edit.as_view(),name='edit'),
]

