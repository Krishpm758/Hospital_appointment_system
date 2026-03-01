from django.shortcuts import render, redirect
from doctor.models import Department, Doctor
from doctor.forms import DoctorForm,DepartmentForm
# Create your views here.
from django.views import View


class Departmentview(View):
    def get(self, request):
        d = Department.objects.all()
        context = {'departments': d}
        return render(request, 'department.html', context)


class DoctorView(View):
    def get(self, request, i):
        c = Doctor.objects.filter(department=i)
        context = {'doctors': c}
        return render(request, 'doctor.html', context)


class Alldoctor(View):
    def get(self, request):
        o = Doctor.objects.all()
        context = {'doc': o}
        return render(request, 'alldoc.html', context)


class Singledoc(View):
    def get(self, request, i):
        t = Doctor.objects.get(id=i)
        context = {'doctor': t}
        return render(request, 'singledoc.html', context)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from doctor.decorators import admin_required

@method_decorator(admin_required,name='dispatch')
@method_decorator(login_required,name='dispatch')
class AddDepartment(View):
    def post(self,request):
        form_instance=DepartmentForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('patients:home')
        else:
            print('error')
            return render(request,'adddept.html',{'form':form_instance})

    def get(self,request):
        form_instance=DepartmentForm()
        context={'form':form_instance}
        return render(request,'adddept.html',context)
    
@method_decorator(login_required,name='dispatch')
class AddDoctor(View):
    def post(self, request):
        form_instance = DoctorForm(request.POST, request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('patients:home')
        else:
            print('error')
            return render(request, 'adddoc.html', {'form': form_instance})

    def get(self, request):
        form_instance = DoctorForm()
        context = {'form': form_instance}
        return render(request, 'adddoc.html', context)

@method_decorator(login_required,name='dispatch')
class Edit(View):
    def post(self,request,i):
        t= Doctor.objects.get(id=i)
        form_instance=DoctorForm(request.POST,request.FILES,instance=t)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('doctor:alldoc')
        context = {'form': form_instance}
        return render(request, 'editdoc.html', context)
    
    def get(self,request,i):
        t=Doctor.objects.get(id=i)
        form_instance=DoctorForm(instance=t)
        context={'form':form_instance}
        return render(request,'editdoc.html',context)
        

