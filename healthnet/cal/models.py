from django.db import models
from django.forms import ModelForm, DateTimeField
from users.models import Patient, Doctor, Person
import datetime

class Appointment(models.Model):
    description = models.CharField(max_length=1000)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.date.today)

class AppointmentForm(ModelForm):
    time = DateTimeField()
    class Meta:
        model = Appointment
        fields = '__all__'
