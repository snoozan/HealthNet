from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from .models import AppointmentForm

@login_required
@transaction.atomic
def show_calendar(request):
    if request.user.person.is_patient:
        #All patient's appointments
        appointments = None
    elif request.user.person.is_doctor:
        #All doctor's appointments
        appointments = None
    elif request.user.person.is_nurse:
        #All appointments for the day at hospital
        appointments = None
    else:
        appointment = []
    return render(request, 'cal/calendar.html', {'appointments':appointments})

@login_required
@transaction.atomic
def create_appointment(request):
    if request.method == 'POST':
        if request.user.person.is_patient:
            appointment_form = AppointmentForm(initial={patient:request.user})
        if request.user.person.is_doctor:
            appointment_form = AppointmentForm(initial={doctor:request.user})
    else:
        appointment_form = AppointmentForm

    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})

@login_required
@transaction.atomic
def delete_appointment(request):
    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})#show_calendar

@login_required
@transaction.atomic
def edit_appointment(request):
    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})
