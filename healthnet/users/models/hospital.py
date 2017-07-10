from django.db import models
from django.forms import ModelForm

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=80)

    patients = models.ManyToManyField('Patient')
    doctors = models.ManyToManyField('Doctor')
    nurses = models.ManyToManyField('Nurse')
    admins = models.ManyToManyField('Admin')

class HospitalForm(ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
