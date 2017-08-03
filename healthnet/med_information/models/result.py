from django.db import models
from django.forms import ModelForm, ModelChoiceField
from users.models import Doctor
from users.models import Patient
from django.utils import timezone


class Result(models.Model):
    test_date = models.DateTimeField(default=timezone.now(), null=True)
    title = models.CharField(max_length=80)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    comments = models.TextField(max_length=1000)
    released = models.BooleanField(default=False)

    #def __str__(self):
        #return self.title


class ResultForm(ModelForm):
    # FIXME filter by hospital
    #patient = ModelChoiceField(queryset=Patient.objects.all())

    class Meta:
        model = Result
        fields = ['title', 'patient', 'comments', 'released']
