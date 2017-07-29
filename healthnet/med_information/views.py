from django.shortcuts import render

# Create your views here.

def admitted(request):
    if request.method == 'GET':

    return render(request, 'med_information/result.html', {'result_form':result_form})
