from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import render, redirect

from .models.prescription import PrescriptionForm, Prescription
from django.contrib import messages
from .models.result import Result, ResultForm
from .models.record import Record, RecordForm
from users.models.person import Doctor, Patient


@login_required
@transaction.atomic
def createPrescription(request, patientid=None):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        del prescription_form.fields['patient']
        if prescription_form.is_valid():
            prescription = prescription_form.save()
            if request.user.person.is_doctor:
                prescription.doctor = Doctor.objects.get(id=request.user.person.id)
            if patientid is not None:
                prescription.patient = Patient.objects.get(id=patientid)
            else:
                print('patient id doesnt exist')
            prescription.save()

        else:
            print('Form not valid')

        return redirect('view_prescription', patientid=patientid)

    else:
        prescription_form = PrescriptionForm()
        if patientid is not None:
            del prescription_form.fields['patient']
        return render(request, 'med_information/prescription.html', {'PrescriptionForm':prescription_form})

@login_required
@transaction.atomic
def updatePrescription(request, prescriptionid):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        del prescription_form.fields['startDate']
        del prescription_form.fields['patient']

        if prescription_form.is_valid():
            prescription = Prescription.objects.get(id=prescriptionid)
            if request.user.person.is_doctor:
                prescription.title = prescription_form.cleaned_data['title']
                prescription.duration = prescription_form.cleaned_data['duration']
                prescription.instructions = prescription_form.cleaned_data['instructions']
                prescription.save()
                messages.success(request, "Prescription Updated!")
                return redirect('view_prescription', patientid=prescription.patient.id)
        else:
            print('houston we have an error')
    else:
        prescription_form = PrescriptionForm(instance=Prescription.objects.get(id=prescriptionid))
        del prescription_form.fields['startDate']
        del prescription_form.fields['patient']

    return render(request, 'med_information/prescription.html', {'PrescriptionForm':prescription_form, 'prescriptionid':prescriptionid})



@login_required
@transaction.atomic
def viewPrescription(request, patientid=None):
    if patientid is not None:
        patient = Patient.objects.get(id = patientid)
    else:
        patient = Patient.objects.get(user = request.user)

    prescriptions = Prescription.objects.filter(patient=patient)

    return render(request, 'med_information/viewPrescriptions.html', {'prescriptions':prescriptions, 'patient':patient})


@login_required
@transaction.atomic
def createTestResult(request, patientid=None):
    if request.method == 'POST':
        result_form = ResultForm(request.POST)
        del result_form.fields['patient']
        if result_form.is_valid():
            result = result_form.save()
            if request.user.person.is_doctor:
                result.doctor = Doctor.objects.get(id=request.user.person.id)
            if patientid is not None:
                print('patient set, id exists')
                result.patient = Patient.objects.get(id=patientid)
            else:
                print('patient id doesnt exist')
            result.save()

        else:
            print('Form not valid')

        return redirect('view_result', patientid=patientid)

    else:
        result_form = ResultForm()
        if patientid is not None:
            del result_form.fields['patient']
        return render(request, 'med_information/result.html', {'ResultForm':result_form})


@login_required
@transaction.atomic
def updateTestResult(request, resultid):
    if request.method == 'POST':
        result_form = ResultForm(request.POST)
        del result_form.fields['patient']

        if result_form.is_valid():
            result = Result.objects.get(id=resultid)
            if request.user.person.is_doctor:
                result.title = result_form.cleaned_data['title']
                result.comments = result_form.cleaned_data['comments']
                result.released = result_form.cleaned_data['released']
                result.save()
                messages.success(request, "Test Result Updated!")
                return redirect('view_result', patientid=result.patient.id)
        else:
            print('Form not valid')
    else:
        result_form = ResultForm(instance=Result.objects.get(id=resultid))
        del result_form.fields['patient']

    return render(request, 'med_information/result.html', {'ResultForm':result_form, 'resultid':resultid})


@login_required
@transaction.atomic
def viewTestResult(request, patientid=None):
    if patientid is not None:
        patient = Patient.objects.get(id=patientid)
    else:
        patient = Patient.objects.get(user=request.user)

    results = Result.objects.filter(patient=patient)

    return render(request, 'med_information/viewResults.html', {'results':results, 'patient':patient})


@login_required
@transaction.atomic
def createRecord(request, patientid=None):
    if request.method == 'POST':
        record_form = RecordForm(request.POST)
        del record_form.fields['patient']

        if record_form.is_valid():
            record = record_form.save()
            if request.user.person.is_doctor:
                record.doctor = Doctor.objects.get(id=request.user.person.id)
            if patientid is not None:
                record.patient = Patient.objects.get(id=patientid)
            else:
                print('patient id doesnt exist')
            record.save()
        else:
            print('Form is not valid')
        return redirect('view_record', patientid=patientid)

    else:
        record_form = RecordForm()
        if patientid is not None:
            del record_form.fields['patient']

        return render(request, 'med_information/record.html', {'RecordForm':record_form})

@login_required
@transaction.atomic
def viewRecord(request, patientid=None):
    if patientid is not None:
        patient = Patient.objects.get(id=patientid)
    else:
        patient = Patient.objects.get(user=request.user)

    records = Record.objects.filter(patient=patient)

    return render(request, 'med_information/viewRecords.html', {'records': records, 'patient': patient})


@login_required
@transaction.atomic
def updateRecord(request, recordid):
    if request.method == 'POST':
        record_form = RecordForm(request.POST)
        del record_form.fields['patient']
        del record_form.fields['startDate']

        if record_form.is_valid():
            record = Record.objects.get(id=recordid)
            if request.user.person.is_doctor:
                record.endDate = record_form.cleaned_data['endDate']
                record.height = record_form.cleaned_data['height']
                record.weight = record_form.cleaned_data['weight']
                record.blood_pressure = record_form.cleaned_data['blood_pressure']
                record.heart_rate = record_form.cleaned_data['heart_rate']
                record.respirations_minute = record_form.cleaned_data['respirations_minute']
                record.reason = record_form.cleaned_data['reason']
                record.description = record_form.cleaned_data['description']
                record.save()
                messages.success(request, "Record Updated!")
                return redirect('view_record', patientid=record.patient.id)
        else:
            print('Form not valid')
    else:
        record_form = RecordForm(instance=Record.objects.get(id=recordid))
        del record_form.fields['patient']
        del record_form.fields['startDate']

    return render(request, 'med_information/record.html', {'RecordForm':record_form, 'recordid':recordid})


