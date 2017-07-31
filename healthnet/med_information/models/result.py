from django.db import models
from django.forms import ModelForm
from users.models import Doctor
from users.models import Patient


class Result(models.Model):
    test_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    comments = models.CharField(max_length=100)
    released = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = ['title', 'comments', 'released']
