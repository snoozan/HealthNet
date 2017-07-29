from django.db import models
from django.utils import timezone
from users.models.person import Patient, Doctor
from users.models.hospital import Hospital
from django.forms import ModelForm, DateField, Widget, ModelChoiceField


class Prescription(models.Model):

    title = models.CharField(max_length=1000)

    startDate = models.DateField(default=timezone.now, null=True)

    duration = models.DurationField(default=0)

    instructions = models.CharField(max_length=1000, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)

#     class Meta:
#         permissions = (
#             ("PatientViewing", "DoctorViewing", "NurseViewing"),
#                        )


class PrescriptionForm(ModelForm):
    patient = ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Prescription
        fields = ('title', 'patient', 'startDate', 'duration', 'instructions')
