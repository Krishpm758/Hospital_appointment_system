from django import forms
from doctor.models import Doctor,Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name','description','image']
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
    