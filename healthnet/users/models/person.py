from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, DateField, Widget
import datetime
from .hospital import Hospital

class PersonManager(models.Manager):
    def get_by_natural_key(self, name, last_name):
        return self.get(name=name)

class Person(models.Model):
    objects = PersonManager()
    name = models.CharField(max_length=100, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_nurse = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    class Meta:
        permissions = (
                ("signup", "Signup as a user"),
        )

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance)
        instance.person.is_patient = True
        content_type = ContentType.objects.get_for_model(Patient)
        permission = Permission.objects.get(
            codename='update_patient',
            content_type=content_type,
        )
        instance.user_permissions.add(permission)
        permission = Permission.objects.get(
            codename='update',
            content_type=content_type,
        )
        instance.user_permissions.add(permission)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class Patient(Person):
    dob = models.DateField(default=datetime.date.today)
    admitted = models.BooleanField(default=False)

    class Meta:
        permissions = (
                ("update_patient", "Signup as a user"),
                ("update", "Signup as a user"),
        )

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'hospital', 'dob')

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class Nurse(Person):
    title = models.CharField(max_length=100, blank=True)
    class Meta:
        permissions = (
                ("admit", "Admit patient"),
        )

class NurseForm(ModelForm):
    class Meta:
        model = Nurse
        fields = ('hospital', 'title', 'name')

class Doctor(Person):
    specialty_field = models.CharField(max_length=100, blank=True)
    class Meta:
        permissions = (
                ("admit", "Admit patient"),
                ("release", "Release patient"),
                ("view_cal", "View patient calendar"),
        )

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ('specialty_field', 'hospital', 'name')

class Admin(Person):
    class Meta:
        permissions = (
                ("transfer", "Transfer patient"),
                ("update_patient", "Signup as a user"),
                ("update", "Signup as a user"),
                ("logs", "Look at activity logs"),
        )

class AdminForm(ModelForm):
    class Meta:
        model = Admin
        fields = ('hospital', 'name')
