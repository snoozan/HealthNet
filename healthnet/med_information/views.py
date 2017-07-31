from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import render, redirect

from healthnet.med_information.models import prescription
from .models.prescription import PrescriptionForm, Prescription
from django.contrib import messages
from .models.result import Result, ResultForm
from .models.record import Record, RecordForm
from users.models.person import Doctor, Patient

def createPrescription(request):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)

        if prescription_form.is_valid():
            result = prescription_form.save()
            result.refresh_from_db()
            Prescription.doctor = Doctor.objects.get(id=request.user.person.id)
            result.save()
            return redirect('admitted_patients')

    else:
        prescription_form = PrescriptionForm()
        return render(request, 'med_information/prescription.html', {'PrescriptionForm':prescription_form})

@login_required
@transaction.atomic
def updatePrescription(request, prescriptionid):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        Prescription.objects.get(id=prescriptionid).delete()
        if prescription_form.is_valid():
            if request.user.person.is_doctor:
                prescription.doctor = Doctor.objects.get(user=request.user.id)
                prescription.doctor.save()
                prescription.save()
                messages.success(request, "Prescription Updated!")
                return redirect('viewPrescriptions')
    else:
        prescription_form = PrescriptionForm(instance=Prescription.objects.get(id=prescriptionid))
        if request.user.person.is_doctor:
            del prescription_form.fields['doctor']

    return render(request, 'cal/appointments.html', {'prescriptionForm':prescription_form, 'prescriptionid':prescriptionid})


@login_required
@transaction.atomic
def viewPrescription(request, pkpatientid=None):
    if pkpatientid is not None:
        if request.user.person.is_patient:
            prescription = Prescription.objects.filter(patient=pkpatientid)
        else:
            redirect()
    else:
        if request.user.person.is_doctor or request.user.person.is_nurse:
            prescription = Prescription.objects.filter(patient=request.user.person.id)
        else:
            redirect()
    return render(request, 'med/viewPrescriptions.html', {'prescription':prescription})

def createTestResult(request):
    if request.method == 'POST':
        result_form = ResultForm(request.POST)

        if result_form.is_valid():
            result = result_form.save()
            result.doctor = Doctor.objects.get( id=request.user.person.id )
            result.save()
            return redirect('admitted_patients')

    elif request.method == 'GET':
        result_form = ResultForm()

    return render(request, 'med_information/result.html', {'result_form':result_form})

def createRecord(request):
    if request.method == 'POST':
        record_form = RecordForm(request.POST)

        if record_form.is_valid():
            record = record_form.save()
            record.doctor = Doctor.objects.get(id=request.user.person.id)
            record.save()
            return redirect('admitted_patients')

    elif request.method == 'GET':
        record_form = RecordForm()

    return render(request, 'med_information/record.html', {'record_form': record_form})

