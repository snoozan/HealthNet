from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib import messages
from .models import AppointmentForm, Appointment
from users.models import Person, Doctor, Patient
from django.db import models

@login_required
@transaction.atomic
def show_calendar(request):
    appointments = ""
    if request.user.person.is_patient:
        appointments = Appointment.objects.filter(patient=request.user.person.id)
    elif request.user.person.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.person.id)
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
            messages.success(request, "Appointment Created!")
            return redirect('calendar')
        else:
            messages.error(request, 'Please correct the error')
    else:
        if request.user.person.is_patient:
            appointment_form = AppointmentForm(initial={'patient':request.user.person.id})
            #del appointment_form.fields['patient']
        if request.user.person.is_doctor:
            appointment_form = AppointmentForm(initial={'doctor':request.user.person.id})
            #del appointment_form.fields['doctor']

    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form})


@login_required
@transaction.atomic
def delete_appointment(request, appointmentid):
    Appointment.objects.get(id=appointmentid).delete()
    messages.success(request, "Appointment Removed!")
    return redirect('calendar')

@login_required
@transaction.atomic
def edit_appointment(request, appointmentid):

    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save()
            Appointment.objects.get(id=appointmentid).delete()
            messages.success(request, "Appointment Updated!")
            return redirect('calendar')
    else:
        appointment_form = AppointmentForm(instance=Appointment.objects.get(id=appointmentid))
        if request.user.person.is_patient:
            print(appointment_form.fields['patient'].required)
        else:
            del appointment_form.fields['doctor']
    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form, 'appointment_id':appointmentid})
