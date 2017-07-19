from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib import messages
from .models import AppointmentForm, Appointment
from users.models import Person

@login_required
@transaction.atomic
def show_calendar(request):
    if request.user.person.is_patient:
        appointments = Appointment.objects.filter(patient=request.user.person.id)
    elif request.user.person.is_doctor:
        appointments = Appointment.objects.filter(patient=request.user.person.id)
    elif request.user.person.is_nurse:
        #All appointments for the day at hospital
        appointments = Appointment.objects.all()
    else:
        appointments = None
    return render(request, 'cal/calendar.html', {'appointments':appointments})

@login_required
@transaction.atomic
def create_appointment(request):
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save()
            #appointment.time = appointment_form.cleaned_data['time']
            messages.success(request, "Appointment Created!")
            return redirect('calendar')
        else:
            messages.error(request, 'Please correct the error')
    else:
        if request.user.person.is_patient:
            appointment_form = AppointmentForm(initial={'patient':request.user.person.id})
        if request.user.person.is_doctor:
            appointment_form = AppointmentForm(initial={'doctor':request.user.person.id})

    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})


@login_required
@transaction.atomic
def delete_appointment(request):
    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})#show_calendar

@login_required
@transaction.atomic
def edit_appointment(request):
    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})
