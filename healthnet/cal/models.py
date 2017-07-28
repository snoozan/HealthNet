from django.db import models
from django.utils import timezone
from django.forms import ModelForm, DateTimeField, DateField, TimeField, ModelChoiceField
from users.models import Patient, Doctor, Person, Hospital
from django.core.exceptions import ValidationError

class Appointment(models.Model):
    description = models.CharField(max_length=1000, null=True)

    time_hour = models.CharField(max_length=2,
                                 choices=(('8','8 a.m.'),('9','9 a.m.'),('10','10 a.m.'),('11','11 a.m.'),
                                          ('12','12 p.m.'),('1','1 p.m.'),('2','2 p.m.'),('3','3 p.m.'),
                                            ('4','4 p.m.'),('5','5 p.m.')),
                                 default='12',
                                null = True)
    time_min = models.CharField(max_length=2,
                                choices=(('00','00'),('30', '30')),
                                default='00',
                               null=True)

    date = models.DateField(default=timezone.now, null=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)


class AppointmentForm(ModelForm):
    patient = ModelChoiceField(required=False, queryset=Patient.objects.all())
    doctor = ModelChoiceField(required=False, queryset=Doctor.objects.all())

    def doesnt_collide(self):#Can collide with own appts different doctors
        doc_appts = Appointment.objects.filter(doctor=self.cleaned_data['doctor'])
        collision = False
        for appt in doc_appts:
            if self.cleaned_data['time_hour'] == appt.time_hour and self.cleaned_data['time_min'] == appt.time_min and self.cleaned_data['date'] == appt.date:
                collision = True
        return not collision
    class Meta:
        model = Appointment
        fields = ('description', 'doctor', 'patient','time_hour', 'time_min', 'date')
