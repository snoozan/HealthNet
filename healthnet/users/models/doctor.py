from .models import Person

class Doctor(Person):
    specialty_field = moels.CharField(max_length=100)

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
