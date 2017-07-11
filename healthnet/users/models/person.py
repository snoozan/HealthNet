from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, DateField
import datetime
from .hospital import Hospital

class Person(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    class Meta:
        permissions = (
                ("signup", "Signup as a user"),
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
    instance.Person.save()

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class Patient(Person):
    dob = DateField(initial=datetime.date.today)
    admitted = models.BooleanField(default=False)

    class Meta:
        permissions = (
                ("update_patient", "Signup as a user"),
        )

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class SignupForm(UserCreationForm):
    birth_date = DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User 
        fields = ('username', 'birth_date', 'password1', 'password2', )


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
