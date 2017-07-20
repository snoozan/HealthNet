from django.db import models
from django.utils import timezone
from django.forms import ModelForm, DateTimeField, DateField, TimeField
from users.models import Patient, Doctor, Person
import datetime

class Appointment(models.Model):
    description = models.CharField(max_length=1000)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=timezone.now)
class AppointmentForm(ModelForm):
    day = DateField()
    time = TimeField()
    class Meta:
        model = Appointment
        fields = ('description', 'patient', 'doctor','time')
