from django.shortcuts import render
from .models.prescription import Prescription
from .models.result import Result
# Create your views here.

def admitted(request):
    if request.method == 'GET':
        results = Result.objects.all()
        prescriptions = Prescription.objects.all()
    elif request.method == 'POST':
        print('posted admitted')
    return render(request, 'med_information/medical_info.html', {'results':results, 'prescriptions':prescriptions})

def prescription(request):
    return render(request, 'med_information/prescription')

