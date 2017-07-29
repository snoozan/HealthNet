from django.shortcuts import render, redirect
from .models.prescription import Prescription
from .models.result import Result, ResultForm

def admitted(request):
    if request.method == 'GET':
        results = Result.objects.all()
        prescriptions = Prescription.objects.all()
    elif request.method == 'POST':
        print('posted admitted')
    return render(request, 'med_information/medical_info.html', {'results':results, 'prescriptions':prescriptions})

def prescription(request):
    return render(request, 'med_information/prescription')



def createTestResult(request):
    if request.method == 'POST':
        result_form = ResultForm(request.POST)

        if result_form.is_valid():
            result = result_form.save()
            result.refresh_from_db()
            result.save()
            return redirect('admitted_patients')

    elif request.method == 'GET':
        result_form = ResultForm()

    return render(request, 'med_information/result', {'result_form':result_form} )
