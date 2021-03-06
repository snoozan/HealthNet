import datetime

import logging
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import render, redirect

from .models.prescription import PrescriptionForm, Prescription
from django.contrib import messages
from .models.result import Result, ResultForm
from .models.record import Record, RecordForm
from users.models.person import Doctor, Patient


@permission_required('users.view_med_info')
@login_required
def viewMedical(request, patientid=None):
    if request.method == 'GET':
        if patientid is not None:
            patient = Patient.objects.get(id=patientid)
        else:
            if request.user.person.is_patient:
                patient = request.user.person.patient
            else:
                redirect('home')
        records = Record.objects.filter(patient=patient)
        results = Result.objects.filter(patient=patient)
        prescriptions = Prescription.objects.filter(patient=patient)
        return render(request, 'med_information/medical_info.html', {'patient':patient, 'records':records, 'results':results, 'prescriptions':prescriptions})


@permission_required('users.create_med_info')
@login_required
@transaction.atomic
def createPrescription(request, patientid=None):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        del prescription_form.fields['patient']
        loggerName = "UoR" if "UoR" in request.user.person.hospital.name else "Strong"
        logger = logging.getLogger(loggerName)
        if prescription_form.is_valid():
            prescription = prescription_form.save()
            if request.user.person.is_doctor:
                prescription.doctor = Doctor.objects.get(id=request.user.person.id)
            if patientid is not None:
                prescription.patient = Patient.objects.get(id=patientid)
            else:
                print('patient id doesnt exist')
            prescription.save()
            logger.info('Created Prescription : {prescription} for {patient} by {user}:Doctor'.format(
                user=request.user.person.name,
                patient=prescription.patient.name,
                prescription=prescription.title
            ))

        else:
            print('Form not valid')

        return redirect('view_medical', patientid=patientid)

    else:
        prescription_form = PrescriptionForm()
        if patientid is not None:
            del prescription_form.fields['patient']
            pname = Patient.objects.get(id=patientid)
        else:
            pname = None
        return render(request, 'med_information/prescription.html', {'PrescriptionForm':prescription_form, 'patient_name': pname})


@permission_required('users.update_med_info')
@login_required
@transaction.atomic
def updatePrescription(request, prescriptionid):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        del prescription_form.fields['startDate']
        del prescription_form.fields['patient']
        loggerName = "UoR" if "UoR" in request.user.person.hospital.name else "Strong"
        logger = logging.getLogger(loggerName)

        if prescription_form.is_valid():
            prescription = Prescription.objects.get(id=prescriptionid)
            if request.user.person.is_doctor:
                prescription.title = prescription_form.cleaned_data['title']
                prescription.duration = prescription_form.cleaned_data['duration']
                prescription.instructions = prescription_form.cleaned_data['instructions']
                prescription.save()
                logger.info('Updated Prescription : {prescription} for {patient} by {user}:Doctor'.format(
                    user=request.user.person.name,
                    patient=Prescription.objects.get(id=prescriptionid).patient.name,
                    prescription=prescription.title
                ))
                messages.success(request, "Prescription Updated!")
                return redirect('view_medical', patientid=prescription.patient.id)
        else:
            print('houston we have an error')
    else:
        prescription_form = PrescriptionForm(instance=Prescription.objects.get(id=prescriptionid))
        del prescription_form.fields['startDate']
        del prescription_form.fields['patient']

    return render(request, 'med_information/prescription.html', {'PrescriptionForm':prescription_form, 'prescriptionid':prescriptionid})




@permission_required('users.create_med_info')
@login_required
@transaction.atomic
def createTestResult(request, patientid=None):
    loggerName = "UoR" if "UoR" in request.user.person.hospital.name else "Strong"
    logger = logging.getLogger(loggerName)
    if request.method == 'POST':
        result_form = ResultForm(request.POST)
        del result_form.fields['patient']
        if result_form.is_valid():
            result = result_form.save()
            if request.user.person.is_doctor:
                result.doctor = Doctor.objects.get(id=request.user.person.id)
            result.patient = Patient.objects.get(id=patientid)
            result.save()
            logger.info('Created Test Result for {patient} by {user}:Doctor'.format(
                user=request.user.person.name,
                patient=Patient.objects.get(id=patientid).name
            ))

        else:
            print('Form not valid')

        return redirect('view_medical', patientid=patientid)

    else:
        result_form = ResultForm()
        if patientid is not None:
            del result_form.fields['patient']
        return render(request, 'med_information/result.html', {'ResultForm':result_form})


@permission_required('users.update_med_info')
@login_required
@transaction.atomic
def updateTestResult(request, resultid):
    loggerName = "UoR" if "UoR" in request.user.person.hospital.name else "Strong"
    logger = logging.getLogger(loggerName)
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
                logger.info('Updated Test Result for {patient} by {user}:Doctor'.format(
                    user=request.user.person.name,
                    patient=Result.objects.get(id=resultid).patient.name
                ))
                messages.success(request, "Test Result Updated!")
                return redirect('view_medical', patientid=result.patient.id)
        else:
            print('Form not valid')
    else:
        result_form = ResultForm(instance=Result.objects.get(id=resultid))
        del result_form.fields['patient']

    return render(request, 'med_information/result.html', {'ResultForm':result_form, 'resultid':resultid})

@permission_required('users.view_med_info')
@login_required
@transaction.atomic
def viewPrescription(request, patientid=None):
    if patientid is not None:
        patient = Patient.objects.get(id = patientid)
    else:
        patient = Patient.objects.get(user = request.user)

    prescriptions = Prescription.objects.filter(patient=patient)

    return render(request, 'med_information/medical_info.html', {'prescriptions':prescriptions, 'patient':patient})
@permission_required('users.view_med_info')
@login_required
@transaction.atomic
def viewRecord(request, patientid=None):
    if patientid is not None:
        patient = Patient.objects.get(id=patientid)
    else:
        patient = Patient.objects.get(user=request.user)

    records = Record.objects.filter(patient=patient)
    print(records)

    return render(request, 'med_information/medical_info.html', {'records': records, 'patient': patient})

@permission_required('users.view_med_info')
@login_required
@transaction.atomic
def viewTestResult(request, patientid=None):
    if patientid is not None:
        patient = Patient.objects.get(id=patientid)
    else:
        patient = Patient.objects.get(user=request.user)

    results = Result.objects.filter(patient=patient)

    return render(request, 'med_information/medical_info.html', {'results':results, 'patient':patient})


@permission_required('users.create_med_info')
@login_required
@transaction.atomic
def createRecord(request, patientid=None):
    if request.method == 'POST':
        record_form = RecordForm(request.POST)
        del record_form.fields['patient']
        del record_form.fields['endDate']
        del record_form.fields['discharged']

        if record_form.is_valid():
            record = record_form.save()
            if request.user.person.is_doctor:
                record.doctor = Doctor.objects.get(id=request.user.person.id)
                record.discharged = False
            if patientid is not None:
                record.patient = Patient.objects.get(id=patientid)
                record.patient.admitted = True
                record.patient.save()
            else:
                print('patient id doesnt exist')
            record.save()
        else:
            print('Form is not valid')

        return redirect('view_medical', patientid=patientid)

    else:
        record_form = RecordForm()
        if patientid is not None:
            del record_form.fields['patient']
            del record_form.fields['endDate']
            del record_form.fields['discharged']

        return render(request, 'med_information/record.html', {'RecordForm':record_form})

@permission_required('users.update_med_info')
@login_required
@transaction.atomic
def updateRecord(request, patientid):
    if request.method == 'POST':
        record_form = RecordForm(request.POST)
        del record_form.fields['patient']
        del record_form.fields['endDate']
        del record_form.fields['discharged']

        loggerName = "UoR" if "UoR" in request.user.person.hospital.name else "Strong"
        logger = logging.getLogger(loggerName)
        if record_form.is_valid():
            patient = Patient.objects.get(id = patientid)
            record = Record.objects.get(patient=patient, discharged = False)
            if request.user.person.is_doctor:
                record.height = record_form.cleaned_data['height']
                record.weight = record_form.cleaned_data['weight']
                record.systolic_pressure = record_form.cleaned_data['systolic_pressure']
                record.diastolic_pressure = record_form.cleaned_data['diastolic_pressure']
                record.heart_rate = record_form.cleaned_data['heart_rate']
                record.respirations_minute = record_form.cleaned_data['respirations_minute']
                record.reason = record_form.cleaned_data['reason']
                record.description = record_form.cleaned_data['description']

                record.save()
                logger.info('Updated Record for {patient} by {user}:Doctor'.format(
                    user=request.user.person.name,
                    patient=Patient.objects.get(id=patientid)
                ))
                messages.success(request, "Record Updated!")
                return redirect('view_medical', patientid=record.patient.id)
        else:
            print('Form not valid')
    else:
        patient = Patient.objects.get(id = patientid)
        record = Record.objects.get(patient=patient, discharged = False)
        record_form = RecordForm(instance=Record.objects.get(id=record.id))
        del record_form.fields['patient']
        del record_form.fields['endDate']
        del record_form.fields['discharged']

    return render(request, 'med_information/record.html', {'RecordForm':record_form, 'recordid':record.id})


@permission_required('users.update_med_info')
@login_required
@transaction.atomic
def finalizeRecord(request, patientid):
    if request.method == 'POST':
        record_form = RecordForm(instance=Record.objects.get(patient=patientid, discharged=False))
        del record_form.fields['patient']

        record = Record.objects.get(patient=patientid, discharged=False)
        if request.user.person.is_doctor:
            record.endDate = datetime.datetime.now()
            record.discharged = True
            if patientid is not None:
                record.patient = Patient.objects.get(id=patientid)
                record.patient.admitted = False
                record.patient.save()
            record.save()
            messages.success(request, "Record Updated!")
            return redirect('view_patients')
    else:
        record_form = RecordForm(instance=Record.objects.get(patient=patientid, discharged=False))
        del record_form.fields['patient']

    return render(request, 'med_information/record.html', {'RecordForm': record_form})
