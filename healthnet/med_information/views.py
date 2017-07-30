from django.shortcuts import render, redirect
from .models.prescription import PrescriptionForm, Prescription
from .models.result import Result, ResultForm
from .models.record import Record, RecordForm
from users.models.person import Doctor, Patient

def admitted(request):
    if request.method == 'GET':
        results = Result.objects.all()
        prescriptions = Prescription.objects.all()
        records = Record.objects.all()
    elif request.method == 'POST':
        print('posted admitted')
    return render(request, 'med_information/medical_info.html', {'results':results, 'prescriptions':prescriptions, 'records':records})


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


# def viewPrescription(request, pk=None):
#     if pk is not None:
#         if request.user.person

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

