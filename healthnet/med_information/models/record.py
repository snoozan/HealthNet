from django.db import models
from django.utils import timezone
from django.forms import ModelForm, ModelChoiceField
from users.models.person import Patient, Doctor


class Record(models.Model):
    startDate = models.DateField(auto_now_add=True, null=True)

    endDate = models.DateField(null=True)

    height = models.CharField(max_length=1000, null=True)

    weight = models.CharField(max_length=1000, null=True)

    blood_pressure = models.CharField(max_length=1000, null=True)

    heart_rate = models.CharField(max_length=1000, null=True)

    respirations_minute = models.CharField(max_length=1000, null=True)

    reason = models.CharField(max_length=1000, null=True)

    description = models.CharField(max_length=1000, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)


class RecordForm(ModelForm):
    #patient = ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Record
        fields = ('endDate', 'patient', 'height', 'weight', 'blood_pressure', 'heart_rate',
                  'respirations_minute', 'reason', 'description')
