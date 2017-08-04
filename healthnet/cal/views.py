import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from django.db import transaction
from django.contrib import messages
from .models import AppointmentForm, Appointment
from users.models import Person, Doctor, Patient, Hospital
from django.db import models

@login_required
@transaction.atomic
def view_calendar(request, pk=None):
    now = datetime.datetime.now()
    one_week = now + datetime.timedelta(weeks=1)

    if pk is not None:
        if request.user.person.is_doctor:
            appointments = Appointment.objects.filter(patient=pk)
        elif request.user.person.is_nurse:
            appointments = Appointment.objects.filter(patient=pk, date__range=(now, one_week))
        elif request.user.person.is_patient:
            appointments = Appointment.objects.filter(patient=pk)
        name = Patient.objects.get(person_ptr_id=pk).name
    else:
        if request.user.person.is_patient:
            appointments = Appointment.objects.filter(patient=request.user.person.id)
        elif request.user.person.is_doctor:
            appointments = Appointment.objects.filter(doctor=request.user.person.id)
        elif request.user.person.is_nurse:
            appointments = Appointment.objects.filter(hospital=request.user.person.hospital, date__range=(now, one_week))
        else:
            appointments = None
        name = None

    return render(request, 'cal/calendar.html', {'appointments':appointments, 'name':name,'pid':pk})

@login_required
@transaction.atomic
def create_appointment(request, pid=None):
    error=None
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            if(request.user.person.is_doctor):
                try:
                    appointment_form.cleaned_data['patient'].id
                except AttributeError:
                    error = "Please select a patient."
                    del appointment_form.fields['doctor']
                    return render(request, 'cal/appointments.html', {'create':True,'appointment_form':appointment_form, 'patientid':pid, 'error':error})

            if(request.user.person.is_patient):
                try:
                    appointment_form.cleaned_data['doctor'].id
                except AttributeError:
                    error = "Please select a doctor."
                    del appointment_form.fields['patient']
                    return render(request, 'cal/appointments.html', {'create':True,'appointment_form':appointment_form, 'patientid':pid, 'error':error})


            if request.user.person.is_patient:
                patientid = request.user.person.id
                doctorid  = appointment_form.cleaned_data['doctor'].id
            else:
                doctorid = request.user.person.id
                patientid  = appointment_form.cleaned_data['patient'].id

            if appointment_form.doesnt_collide(patientid, doctorid):
                appointment = appointment_form.save()
                appointment.doctor = Doctor.objects.get(id=doctorid)
                appointment.patient = Patient.objects.get(id=patientid)
                appointment.hospital = Hospital.objects.get(id=request.user.person.hospital_id)

                appointment.save()

                messages.success(request, "Appointment Created!")
                return redirect('calendar')
            else:
                messages.error(request, 'Collision detected')
                if request.user.person.is_patient:
                    del appointment_form.fields['patient']
                elif request.user.person.is_doctor:
                    del appointment_form.fields['doctor']
                error = "Try another time, either you already have an appointment or the doctor is busy at this time!"
    else:#if GET request
        appointment = Appointment.objects.create(hospital = request.user.person.hospital)
        appointment_form = AppointmentForm()

#         if pid is not None:
#             if request.user.person.is_doctor:
#                 appointment.patient = Patient.objects.get(id = pid)
#                 appointment.doctor = Doctor.objects.get(id = request.user.person.id)

#             elif request.user.person.is_patient:#test
#                 appointment.patient = Patient.objects.get(id = pid)

#         else:
#             if request.user.person.is_patient:
#                 appointment.patient = Patient.objects.get(id = request.user.person.id)
#             elif request.user.person.is_doctor:
#                 appointment.doctor = Doctor.objects.get(id = request.user.person.id)

        hospital = request.user.person.hospital

        if pid is not None:
            if request.user.person.is_doctor:
                del appointment_form.fields['doctor']
            elif request.user.person.is_nurse:
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=hospital)
            elif request.user.person.is_patient:
                del appointment_form.fields['patient']
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=hospital)

        else:
            if request.user.person.is_doctor:
                del appointment_form.fields['doctor']
                appointment_form['patient'].queryset = Patient.objects.filter(hospital=hospital)
            elif request.user.person.is_nurse:
                appointment_form['patient'].queryset = Patient.objects.filter(hospital=hospital)
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=hospital)
            elif request.user.person.is_patient:
                del appointment_form.fields['patient']
                appointment_form['doctor'].queryset = Doctor.objects.filter(hospital=hospital)

    return render(request, 'cal/appointments.html', {'create':True,'appointment_form':appointment_form, 'patientid':pid, 'error':error})


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
            if request.user.person.is_patient:
                patientid = request.user.person.id
                doctorid  = appointment_form.cleaned_data['doctor'].id
            else:
                doctorid = request.user.person.id
                patientid  = appointment_form.cleaned_data['patient'].id
            if appointment_form.doesnt_collide(patientid, doctorid):
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
