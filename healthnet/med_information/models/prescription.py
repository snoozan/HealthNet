from django.db import models
from django.utils import timezone
from healthnet.users.models import Patient, Doctor, Person, Hospital
from django.forms import ModelForm, DateField, Widget


class Prescription(models.Model):

    startDate = models.DateField(default=timezone.now, null=True)

    duration = models.DurationField(min(0))

    instructions = models.CharField(max_length=1000, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = (
            ("PatientViewing", "DoctorViewing", "NurseViewing"),
                       )


class PrescriptionForm(ModelForm):

    class Meta:
        model = Prescription
        fields = ('startDate', 'duration', 'instructions')
