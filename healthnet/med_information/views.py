from django.shortcuts import render, redirect
from .models.result import ResultForm

# Create your views here.

def admitted(request):
    if request.method == 'GET':
        print('')
    return render(request, 'med_information/result.html', {'result_form':result_form})

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