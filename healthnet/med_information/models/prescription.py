from django.db import models
from django.utils import timezone
from users.models.person import Patient, Doctor
from django.forms import ModelForm, ModelChoiceField


class Prescription(models.Model):

    title = models.CharField(max_length=1000)

    startDate = models.DateField(default=timezone.now(), null=True)

    duration = models.IntegerField(default="1")

    instructions = models.TextField(max_length=1000, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)

#     class Meta:
#         permissions = (
#             ("PatientViewing", "DoctorViewing", "NurseViewing"),
#                        )


class PrescriptionForm(ModelForm):
    patient = ModelChoiceField(queryset=Patient.objects.all(), required=False)

    class Meta:
        model = Prescription
        fields = ('patient', 'title', 'startDate', 'duration', 'instructions')
