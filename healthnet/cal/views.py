import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from django.db import transaction
from django.contrib import messages
from .models import AppointmentForm, Appointment
from users.models import Person, Doctor, Patient
from django.db import models

@login_required
@transaction.atomic
def show_calendar(request):
    appointments = ""
    appointmentwith=""
    if request.user.person.is_patient:
        appointments = Appointment.objects.filter(patient=request.user.person.id)
    elif request.user.person.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.person.id)
    elif request.user.person.is_nurse:
        #All appointments for the day at hospital
        appointments = Appointment.objects.all()
    else:
        appointments = None
    return render(request, 'cal/calendar.html', {'appointments':appointments, 'person':request.user.person})

@login_required
@transaction.atomic
def view_calendar(request, pk):
    if request.user.person.is_doctor:
        appointments = Appointment.objects.filter(pk=pk)
    else:
        now = datetime.datetime.now()
        two_weeks = now + datetime.timedelta(weeks=2)

        appointments = Appointment.objects.filter(pk, time__range=(now, two_weeks))
    return render(request, 'cal/calendar.html', {'appointments':appointments})

@login_required
@transaction.atomic
def create_appointment(request):
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            if appointment_form.doesnt_collide():
                appointment = appointment_form.save()
                if request.user.person.is_patient:
                    appointment.patient = Patient.objects.get(user = request.user.id)
                    appointment.patient.save()

                elif request.user.person.is_doctor:
                    appointment.doctor = Doctor.objects.get(user=request.user.id)
                    appointment.doctor.save()
                appointment.save()
                messages.success(request, "Appointment Created!")
                return redirect('calendar')
            else:
                if request.user.person.is_patient:
                    del appointment_form.fields['patient']
                    appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=Patient.objects.get(user = request.user).hospital)
                elif request.user.person.is_doctor:
                    del appointment_form.fields['doctor']
                    appointment_form['patient'].queryset = Patient.objects.filter(hospital=Doctor.objects.get(user = request.user).hospital)
        elif request.user.person.is_nurse:
            appointment_form['patient'].queryset = Patient.objects.filter(hospital=appointment.hospital)
            appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=appointment.hospital)
        else:
            messages.error(request, 'Please correct the error')
    else:#if GET request
        appointment = Appointment.objects.create(hospital = request.user.person.hospital)
        appointment_form = AppointmentForm(instance=appointment)

        if request.user.person.is_patient:
            del appointment_form.fields['patient']
            appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=Patient.objects.get(user = request.user).hospital)
        elif request.user.person.is_doctor:
            del appointment_form.fields['doctor']
            appointment_form['patient'].queryset = Patient.objects.filter(hospital=Doctor.objects.get(user = request.user).hospital)

        elif request.user.person.is_nurse:
            appointment_form['patient'].queryset = Patient.objects.filter(hospital=appointment.hospital)
            appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=appointment.hospital)
        else:
            appointment_form, appointment = "",""

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
        Appointment.objects.get(id=appointmentid).delete()
        if appointment_form.is_valid():
            if appointment_form.doesnt_collide():
                appointment=appointment_form.save()
                if request.user.person.is_patient:
                    appointment.patient = Patient.objects.get(user = request.user.id)
                    appointment.patient.save()

                elif request.user.person.is_doctor:
                    appointment.doctor = Doctor.objects.get(user=request.user.id)
                    appointment.doctor.save()
                appointment.save()

                messages.success(request, "Appointment Updated!")
                return redirect('calendar')
            else:#appointment collides
                if request.user.person.is_patient:
                    del appointment_form.fields['patient']
                elif request.user.person.is_doctor:
                    del appointment_form.fields['doctor']

    else:
        appointment_form = AppointmentForm(instance=Appointment.objects.get(id=appointmentid))
        if request.user.person.is_patient:
            del appointment_form.fields['patient']
        elif request.user.person.is_doctor:
            del appointment_form.fields['doctor']

    return render(request, 'cal/appointments.html', {'appointment_form':appointment_form, 'appointment_id':appointmentid})
