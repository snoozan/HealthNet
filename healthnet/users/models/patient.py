from .models import Person

class Patient(Person):
    dob = models.DateField(max_length=8)
    admitted = models.BooleanField(default=False)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
