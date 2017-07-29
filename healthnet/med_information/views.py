from django.shortcuts import render

# Create your views here.

def admitted(request):
    return render(request, 'med_information/result.html')

def prescription(request):
    return render(request, 'med_information/prescription')