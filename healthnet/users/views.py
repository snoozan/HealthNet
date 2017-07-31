from DateTime import DateTime
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

import logging

from users.models import Hospital
from .models.person import PatientForm, SignupForm, DoctorForm, NurseForm, AdminForm, Admin, Nurse
from .models.person import Patient, Doctor, Person

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):

    logger = logging.getLogger('patient_login')
    logger.info('login user: {user}'.format(
        user=user.person.name,
    ))

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):

    logger = logging.getLogger('patient_login')
    logger.info('logout user: {user}'.format(
        user=user.person.name,
    ))


# Create your views here.
@login_required
def home(request):
    if request.user.person.is_patient:
        if not request.user.person.patient.name:
            return redirect("update_patient")
    if request.user.person.is_doctor:
        profile_form = DoctorForm(instance=request.user.person)
    elif request.user.person.is_nurse:
        profile_form = NurseForm(instance=request.user.person)
    elif request.user.person.is_admin:
        profile_form = AdminForm(instance=request.user.person)
    else:
        profile_form = PatientForm(instance=request.user.person)

    return render(request, 'users/home.html', {
        'profile_form': profile_form,
    })


@login_required
@permission_required('users.update_patient')
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=request.user.person)
        if patient_form.is_valid():
            patient_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        patient_form = PatientForm(instance=request.user.person)
        hospitals = Hospital.objects.all()
    return render(request, 'users/profile.html', {
        'patient_form': patient_form,
        'hospitals': hospitals
    })


@transaction.atomic
def signup_patient(request):
    if request.method == 'POST':
        patient_form = SignupForm(request.POST)
        if patient_form.is_valid():
            patient = patient_form.save()
            patient.refresh_from_db()
            patient.save()
            raw_password = patient_form.cleaned_data.get('password1')
            user = authenticate(username=patient.username, password=raw_password)
            login(request, user)
            messages.success(request, 'You successfully signed up!')
            return redirect('home')
        else: messages.error(request, 'Please correct the error below.')
    else:
        patient_form = SignupForm()
    return render(request, 'users/signup.html', {
        'patient_form': patient_form
    })

@permission_required('users.update')
@login_required
def update(request):
   nurses = Nurse.objects.filter(hospital=request.user.person.hospital_id)
   doctors = Doctor.objects.filter(hospital=request.user.person.hospital_id)
   admins = Admin.objects.filter(hospital=request.user.person.hospital_id)
   return render(request, 'users/update.html', {
       'nurses' : nurses,
       'doctors': doctors,
       'admins': admins,
   })


@permission_required('users.update')
@login_required
@transaction.atomic
def update_nurse(request, pk):
    if request.method == 'POST':
        nurse_form = NurseForm(request.POST, instance=Nurse.objects.get(pk=pk))
        if nurse_form.is_valid():
            nurse_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        nurse_form = NurseForm(instance=Nurse.objects.get(pk=pk))
    return render(request, 'users/profile.html', {
        'nurse_form': nurse_form,
    })

@permission_required('users.update')
@login_required
@transaction.atomic
def update_doctor(request, pk):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, instance=Doctor.objects.get(pk=pk))
        if doctor_form.is_valid():
            doctor_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        doctor_form = DoctorForm(instance=Doctor.objects.get(pk=pk))
    return render(request, 'users/profile.html', {
        'doctor_form': doctor_form,
    })


@permission_required('users.update')
@login_required
@transaction.atomic
def update_admin(request, pk):
    if request.method == 'POST':
        admin_form = AdminForm(request.POST, instance=Admin.objects.get(pk=pk))
        if admin_form.is_valid():
            admin_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        admin_form = AdminForm(instance=Admin.objects.get(pk=pk))
    return render(request, 'users/profile.html', {
        'admin_form': admin_form,
    })


@permission_required('users.update')
@login_required
@transaction.atomic
def create_nurse(request):
    if request.method == 'POST':
        nurse_form = NurseForm(request.POST)
        account_form = SignupForm(request.POST)
        if account_form.is_valid() and nurse_form.is_valid():
            user = account_form.save()
            Person.objects.get(pk=user.person.id).delete()
            nurse = Nurse.objects.create(user=user)
            nurse.name = nurse_form.cleaned_data.get('name')
            nurse.hospital = Hospital.objects.get(pk=request.user.person.hospital_id)
            nurse.title = nurse_form.cleaned_data.get('title')
            nurse.is_nurse = True
            content_type = ContentType.objects.get_for_model('Doctor')
            permission = Permission.objects.get(
                codename='admit',
                content_type=content_type,
            )
            nurse.user.user_permissions.add(permission.id)
            content_type = ContentType.objects.get_for_model('Doctor')
            permission = Permission.objects.get(
                codename='release',
                content_type=content_type,
            )
            nurse.user.user_permissions.add(permission.id)
            content_type = ContentType.objects.get_for_model('Doctor')
            permission = Permission.objects.get(
                codename='view_calendar',
                content_type=content_type,
            )
            nurse.user.user_permissions.add(permission.id)
            nurse.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        nurse_form = NurseForm()
        account_form = SignupForm()
    return render(request, 'users/profile.html', {
        'nurse_form': nurse_form,
        'account_form': account_form
    })


@permission_required('users.update')
@login_required
@transaction.atomic
def create_doctor(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)
        account_form = SignupForm(request.POST)
        if account_form.is_valid() and doctor_form.is_valid():
            user = account_form.save()
            Person.objects.get(pk=user.person.id).delete()
            doctor = Doctor.objects.create(user=user)
            doctor.name = doctor_form.cleaned_data.get('name')
            doctor.specialty_field = doctor_form.cleaned_data.get('specialty_field')
            doctor.hospital = Hospital.objects.get(pk=request.user.person.hospital_id)
            doctor.is_doctor = True
            content_type = ContentType.objects.get_for_model('Doctor')
            permission = Permission.objects.get(
                codename='admit',
                content_type=content_type,
            )
            doctor.user.user_permissions.add(permission.id)
            content_type = ContentType.objects.get_for_model('Doctor')
            permission = Permission.objects.get(
                codename='release',
                content_type=content_type,
            )
            doctor.user.user_permissions.add(permission.id)
            content_type = ContentType.objects.get_for_model('Doctor')
            permission = Permission.objects.get(
                codename='view_calendar',
                content_type=content_type,
            )
            doctor.user.user_permissions.add(permission.id)
            doctor.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        doctor_form = DoctorForm()
        account_form = SignupForm()
    return render(request, 'users/profile.html', {
        'doctor_form': doctor_form,
        'account_form': account_form
    })


@permission_required('users.update')
@login_required
@transaction.atomic
def create_admin(request):
    if request.method == 'POST':
        admin_form = DoctorForm(request.POST)
        account_form = SignupForm(request.POST)
        if account_form.is_valid() and admin_form.is_valid():
            user = account_form.save()
            Person.objects.get(pk=user.person.id).delete()
            admin = Admin.objects.create(user=user)
            admin.name = admin_form.cleaned_data.get('name')
            admin.hospital = Hospital.objects.get(pk=request.user.person.hospital_id)
            admin.is_admin = True
            admin.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        admin_form = AdminForm()
        account_form = SignupForm()
    return render(request, 'users/profile.html', {
        'doctor_form': admin_form,
        'account_form': account_form
    })


@permission_required('users.admit')
@login_required
@transaction.atomic
def admit_patient(request):
    logger = logging.getLogger('admit_patient')
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.POST.get('id'))
        patient.admitted = True
        patient.save()
        messages.success(request, 'Patient was successfully admitted!')
        logger.info('Admit patient:{patient} by {user}:{type} to {currHospital}'.format(
            patient = patient.name,
            user= request.user.person.name,
            type = request.user.person,
            currHospital = request.user.person.hospital.name,
        ))

    patients = Patient.objects.filter(Q(hospital=request.user.person.hospital_id, admitted=False) | Q(admitted=False)).exclude(
       (Q(name__isnull=True) | Q(name__exact=''))
    )

    return render(request, 'users/admit.html', {
        'patients': patients,
        'admit': True
    })

@permission_required('users.admit')
@login_required
@transaction.atomic
def view_patients(request):
    if(request.user.person.is_nurse):
        patients = Patient.objects.filter(hospital=request.user.person.hospital_id)
    else:
        patients = Patient.objects.all()

    return render(request, 'users/patients.html', {
        'patients': patients,
    })



@permission_required('users.release')
@login_required
@transaction.atomic
def release_patient(request):
    logger = logging.getLogger('discharge_patient')
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.POST.get('id'))
        patient.admitted = False
        patient.save()
        messages.success(request, 'Patient was successfully admitted!')
        type = "nurse" if request.user.person.is_nurse else "doctor"
        logger.info('Discharge patient:{patient} by {user}:{type} to {currHospital}'.format(
            patient = patient.name,
            user= request.user.name,
            type = type,
            currHospital = request.user.person.hospital.name,
        ))

    patients = Patient.objects.order_by('hospital').filter(hospital=request.user.person.hospital_id, admitted=True)

    return render(request, 'users/admit.html', {
        'patients': patients,
        'admit': False
    })

@permission_required('users.transfer')
@login_required
@transaction.atomic
def transfer_view(request):
    if(request.user.person.is_admin):
        patients = Patient.objects.filter(hospital=request.user.person.hospital_id)
    return render(request, 'users/patients.html', {
        'patients': patients,
        'transfer': True
    })


@permission_required('users.transfer')
@login_required
@transaction.atomic
def transfer_patient(request, pk):
    logger = logging.getLogger('patient_transfer')
    if request.method == 'POST':
        patient = Patient.objects.get(pk=pk)
        patient_form = PatientForm(request.POST, instance=patient)
        if(patient_form.is_valid()):
            patient.admitted = False
            patient_form.save()
            messages.success(request, 'Patient was transferred successfully!')
            hospitals = Hospital.objects.exclude(pk=Patient.objects.get(pk=pk).hospital_id)
            type = "admin" if request.user.person.is_admin else "doctor"
            logger.info('transfer patient:{patient} by {user}:{type} from {currHospital} to {newHospital}'.format(
                patient = patient.name,
                user= request.user.person.name,
                type = type,
                currHospital = request.user.person.hospital.name,
                newHospital = patient.hospital.name
            ))
        else:
            messages.error(request, 'Incorrectly formatted request.')

    else:
        if(request.user.person.is_admin):
            hospitals = Hospital.objects.exclude(pk=Patient.objects.get(pk=pk).hospital_id)
        else:
            hospitals = Hospital.objects.get(pk=request.user.person.hospital_id)
        patient = Patient.objects.get(pk=pk)
    return render(request, 'users/transfer.html', {
        'hospitals': hospitals,
        'patient': patient,
    })
