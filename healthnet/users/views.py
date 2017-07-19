from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction

from users.models import Hospital
from .models.person import PatientForm, SignupForm, DoctorForm, NurseForm, AdminForm, Admin, Nurse
from .models.person import Patient, Doctor, Person


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
    return render(request, 'users/profile.html', {
        'patient_form': patient_form,
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
            nurse.hospital = request.user.person.hospital_id
            nurse.title = nurse_form.cleaned_data.get('title')
            nurse.is_nurse = True
            nurse.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users/profile')
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
            doctor.hospital = request.user.person.hospital_id
            doctor.is_doctor = True
            doctor.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users/profile')
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
            admin.is_admin = True
            admin.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        admin_form = AdminForm()
        account_form = SignupForm()
    return render(request, 'users/profile.html', {
        'doctor_form': admin_form,
        'account_form': account_form
    })


@permission_required('admit')
@login_required
@transaction.atomic
def admit_patient(request):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.patientid)
        patient.admitted = True
        patient.save()
        messages.success(request, 'Patient was successfully admitted!')
    else:
        messages.error(request, 'Incorrectly formatted request.')

    return render(request, 'profiles/profile.html')


@permission_required('users.release')
@login_required
@transaction.atomic
def release_patient(request):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.patientid)
        patient.admitted = False
        patient.save()
    else:
        messages.error(request, 'Incorrectly formatted request.')

    return render(request, 'users/profile.html')

@permission_required('users.transfer')
@login_required
@transaction.atomic
def transfer_view(request):
    patients = Patient.objects.filter(hospital=request.user.person.hospital_id)
    return render(request, 'users/patients.html', {
        'patients': patients
    })



@permission_required('users.transfer')
@login_required
@transaction.atomic
def transfer_patient(request, pk):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=pk)
        patient_form = PatientForm(request.POST, instance=patient)
        if(patient_form.is_valid()):
            patient_form.save()
            messages.success(request, 'Patient was transferred successfully!')
        else:
            messages.error(request, 'Incorrectly formatted request.')

    else:
        hospitals = Hospital.objects.exclude(pk=Patient.objects.get(pk=pk).hospital_id)
        patient = Patient.objects.get(pk=pk)
    return render(request, 'users/transfer.html', {
        'hospitals': hospitals,
        'patient': patient,
    })
