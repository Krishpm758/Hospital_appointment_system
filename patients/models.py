from tkinter.constants import CASCADE
from django.db import models
from django.contrib.auth.models import User
from doctor.models import Department, Doctor


# Create your models here.

class BookAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    appointment_date = models.DateField()
    time_slot = models.TimeField()
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    phone = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True)

    @property
    def is_past(self):
        from datetime import datetime
        return datetime.combine(self.appointment_date, self.time_slot) < datetime.now()
    
    def __str__(self):
        return self.name