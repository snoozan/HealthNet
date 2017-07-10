from .models import Patient, Doctor, Nurse, Admin

class Hospital(models.model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=80)

    patients = models.ManyToMany(Patient)
    doctors = models.ManyToMany(Doctor)
    nurses = models.ManyToMany(Nurse)
    admins = models.ManyToMany(Admin)

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
