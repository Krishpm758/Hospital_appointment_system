from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(upload_to='department')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=30)
    image = models.ImageField(upload_to='doctors')
    Education = models.CharField(max_length=30)

    def __str__(self):
        return self.name