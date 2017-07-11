from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm
from .hospital import Hospital

class Person(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
    )
    class Meta:
        permissions = (
                ("signup", "Signup as a user"),
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.Person.save()

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class Patient(Person):
    dob = models.DateField(max_length=8)
    admitted = models.BooleanField(default=False)

    class Meta:
        permissions = (
                ("update_patient", "Signup as a user"),
        )

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class Nurse(Person):
    title = models.CharField(max_length=100)
    class Meta:
        permissions = (
                ("admit", "Admit patient"),
                ("release", "Release patient"),
        )

class NurseForm(ModelForm):
    class Meta:
        model = Nurse
        fields = '__all__'

class Doctor(Person):
    specialty_field = models.CharField(max_length=100)
    class Meta:
        permissions = (
                ("admit", "Admit patient"),
                ("release", "Release patient"),
        )

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class Admin(Person):
    position = models.CharField(max_length=100)
    class Meta:
        permissions = (
                ("transfer", "Transfer patient"),
                ("update", "Update admin/doctor/nurse"),
        )

class AdminForm(ModelForm):
    class Meta:
        model = Admin 
        fields = '__all__'
