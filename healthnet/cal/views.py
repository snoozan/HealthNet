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
def view_calendar(request, pk=None):
    now = datetime.datetime.now()
    two_weeks = now + datetime.timedelta(weeks=1)
    did=None
    pid=None
    if pk is not None:
        if request.user.person.is_doctor:
            appointments = Appointment.objects.filter(patient=pk)
            pid = pk
        elif request.user.person.is_nurse:
            appointments = Appointment.objects.filter(pk, time__range=(now, two_weeks))
            #cannot create appts....
        elif request.user.person.is_patient:
            appointments = Appointment.objects.filter(patient=pk, time__range=(now, two_weeks))
            did = pk
    else:
        if request.user.person.is_patient:
            appointments = Appointment.objects.filter(patient=request.user.person.id)
        elif request.user.person.is_doctor:
            appointments = Appointment.objects.filter(doctor=request.user.person.id)
        elif request.user.person.is_nurse:
            appointments = Appointment.objects.all(hospital=request.user.person.hospital)#same day, TEST!
        else:
            appointments = None

    if pid is not None:
        name = Person.objects.get(id=pid).name
    elif did is not None:
        name = Person.objects.get(id=did).name
    else:
        name = ''
    return render(request, 'cal/calendar.html', {'appointments':appointments, 'pid':pid, 'did':did, 'name':name})

@login_required
@transaction.atomic
def create_appointment(request, pid=None, did=None):
    error=None
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            if appointment_form.doesnt_collide():
                #appointment = appointment_form.save()
                a = Appointment.objects.get(id=request.POST['appointment_id'])
                a.description = appointment_form.cleaned_data['description']
                a.time_hour = appointment_form.cleaned_data['time_hour']
                a.time_min = appointment_form.cleaned_data['time_min']
                a.date = appointment_form.cleaned_data['date']
                if a.doctor is None:
                    a.doctor = appointment_form.cleaned_data['doctor']
                if a.patient is None:
                    a.patient = appointment_form.cleaned_data['patient']
                a.save()

                messages.success(request, "Appointment Created!")
                return redirect('calendar')
            else:
                messages.error(request, 'Collision detected')
                appointmentid=request.POST['appointment_id']
                if request.user.person.is_patient:
                    del appointment_form.fields['patient']
                elif request.user.person.is_doctor:
                    del appointment_form.fields['doctor']
                error = "Try another time, either you already have an appointment or the doctor is busy at this time!"
    else:#if GET request
        appointment = Appointment.objects.create(hospital = request.user.person.hospital)
        if pid is not None:
            if request.user.person.is_doctor:
                appointment.patient = Patient.objects.get(id = pid)
                appointment.doctor = Doctor.objects.get(id = request.user.person.id)
            elif request.user.person.is_nurse:
                appointment.patient = Patient.objects.get(id = pid)
            elif request.user.person.is_patient:#test
                appointment.patient = Patient.objects.get(id = pid)
        elif did is not None:
            if request.user.person.is_doctor:
                appointment.doctor = Doctor.objects.get(id = did)
            elif request.user.person.is_nurse:
                appointment.doctor = Doctor.objects.get(id = did)
            elif request.user.person.is_patient:
                appointment.doctor = Doctor.objects.get(id = did)
                appointment.patient = Patient.objects.get(id = request.user.person.id)
        else:
            if request.user.person.is_patient:
                print(request.user.person.__dict__)
                appointment.patient = Patient.objects.get(id = request.user.person.id)
            elif request.user.person.is_doctor:
                appointment.doctor = Doctor.objects.get(id = request.user.person.id)

        appointment.save()

        appointment_form = AppointmentForm(instance=appointment)
        appointmentid=appointment.id

        if pid is not None:
            if request.user.person.is_doctor:
                del appointment_form.fields['doctor']
            elif request.user.person.is_nurse:
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=appointment.hospital)
            elif request.user.person.is_patient:
                del appointment_form.fields['patient']
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=appointment.hospital)
        elif did is not None:
            if request.user.person.is_doctor:
                del appointment_form.fields['doctor']
                appointment_form['patient'].queryset = Patient.objects.filter(hospital=appointment.hospital)
            elif request.user.person.is_nurse:
                appointment_form['patient'].queryset = Patient.objects.filter(hospital=appointment.hospital)
            elif request.user.person.is_patient:
                del appointment_form.fields['patient']
                del appointment_form.fields['doctor']
        else:
            if request.user.person.is_doctor:
                del appointment_form.fields['doctor']
                appointment_form['patient'].queryset = Patient.objects.filter(hospital=appointment.hospital)
            elif request.user.person.is_nurse:
                appointment_form['patient'].queryset = Patient.objects.filter(hospital=appointment.hospital)
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=appointment.hospital)
            elif request.user.person.is_patient:
                del appointment_form.fields['patient']
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=appointment.hospital)

    return render(request, 'cal/appointments.html', {'create':True,'appointment_form':appointment_form, 'patientid':pid, 'doctorid':did, 'appointment_id':appointmentid, 'error':error})


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
