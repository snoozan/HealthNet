from django.db import models
from django.forms import ModelForm

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class HospitalForm(ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
