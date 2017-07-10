from .models import Person

class Nurse(Person):
    title = models.CharField(max_length=100)

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = '__all__'
