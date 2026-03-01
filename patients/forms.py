from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from doctor.models import Department, Doctor
from patients.models import BookAppointment


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class AppointmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('appointment_date')
        time_slot = cleaned_data.get('time_slot')

        if doctor and appointment_date and time_slot:
            if BookAppointment.objects.filter(
                doctor=doctor, 
                appointment_date=appointment_date, 
                time_slot=time_slot, 
                payment_status=True
            ).exists():
                raise forms.ValidationError("This time slot is already booked. Please choose another one.")
        return cleaned_data

    class Meta:
        model = BookAppointment
        fields = ['doctor', 'department', 'name', 'age', 'phone', 'appointment_date', 'time_slot']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.Select(choices=[
                ('09:00:00', '09:00 AM - 09:30 AM'),
                ('09:30:00', '09:30 AM - 10:00 AM'),
                ('10:00:00', '10:00 AM - 10:30 AM'),
                ('10:30:00', '10:30 AM - 11:00 AM'),
                ('11:00:00', '11:00 AM - 11:30 AM'),
                ('11:30:00', '11:30 AM - 12:00 PM'),
                ('12:00:00', '12:00 PM - 12:30 PM'),
                ('12:30:00', '12:30 PM - 01:00 PM'),
                ('14:00:00', '02:00 PM - 02:30 PM'),
                ('14:30:00', '02:30 PM - 03:00 PM'),
                ('15:00:00', '03:00 PM - 03:30 PM'),
                ('15:30:00', '03:30 PM - 04:00 PM'),
                ('16:00:00', '04:00 PM - 04:30 PM'),
                ('16:30:00', '04:30 PM - 05:00 PM'),
            ], attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }