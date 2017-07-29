from django.shortcuts import render, redirect
from .models.prescription import PrescriptionForm
from users.models import Person, Doctor, Patient

# Create your views here.

def admitted(request):
    if request.method == 'GET':
        print('')
    return render(request, 'med_information/result.html', {'result_form':result_form})


def createPrescription(request):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        return redirect('admitted_patients')
    else:
        prescription_form = PrescriptionForm()
        return render(request, 'med_information/prescription.html', {'PrescriptionForm':PrescriptionForm})


def viewPrescription(request, pk=None):
    if pk is not None:
        if request.user.person
