from django.shortcuts import render

# Create your views here.

def admitted(request):
    if request.method == 'GET':
        print('')
    return render(request, 'med_information/result.html', {'result_form':result_form})

def prescription(request):
    return render(request, 'med_information/prescription')

