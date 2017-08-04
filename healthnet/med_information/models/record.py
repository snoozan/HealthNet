import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, ModelChoiceField
from users.models.person import Patient, Doctor


class Record(models.Model):
    startDate = models.DateTimeField(default=timezone.now(), null=True)

    endDate = models.DateTimeField(null=True, blank=True)

    height = models.PositiveIntegerField(null=True, default=0)

    weight = models.PositiveIntegerField(null=True, default=0)

    systolic_pressure = models.PositiveIntegerField(null=True, default=0)

    diastolic_pressure = models.PositiveIntegerField(null=True, default=0)

    heart_rate = models.PositiveIntegerField(null=True, default=0)

    respirations_minute = models.PositiveIntegerField(null=True, default=0)

    reason = models.CharField(max_length=1000, null=True)

    description = models.TextField(max_length=1000, null=True)

    discharged = models.BooleanField(default=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)


class RecordForm(ModelForm):
    #patient = ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Record
        fields = ('endDate', 'patient', 'height', 'weight', 'systolic_pressure', 'diastolic_pressure', 'heart_rate',
                  'respirations_minute', 'reason', 'description', 'discharged')
