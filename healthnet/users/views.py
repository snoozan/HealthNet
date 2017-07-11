from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from .models.person import PersonForm, PatientForm, SignupForm
from .models.hospital import HospitalForm

# Create your views here.

@permission_required('update_patient')
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        profile_form = PatientForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'patient_form': patient_form,
    })

@transaction.atomic
def create_hospital(request):
    if request.method == 'POST':
        hospital_form = HospitalForm(request.POST)
        if hospital_form.is_valid():
            hospital_form.save()
            messages.success(request, "Hospital successfully created!")
            return redirect('signup')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        hospital_form = HospitalForm
    return render(request, 'users/hospital.html', {
            'hospital_form' : hospital_form,
    })


@transaction.atomic
def signup_patient(request): 
    if request.method == 'POST':
        patient_form = SignupForm(request.POST)
        if patient_form.is_valid():
            patient = patient_form.save()
            patient.refresh_from_db()
            patient.patient.dob = patient_form.cleaned_data.get('dob')
            patient.save()
            raw_password = patient_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users/login.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        patient_form = SignupForm()

    return render(request, 'users/signup.html', {
        'patient_form': patient_form
    })

@permission_required('update')
@login_required
@transaction.atomic
def update_nurse(request): 
    if request.method == 'POST':
        nurse_form = NurseForm(request.POST, instance=request.user.profile)
        if nurse_form.is_valid():
            nurse_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        nurse_form = NurseForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'nurse_form': nurse_form
    })

@permission_required('update')
@login_required
@transaction.atomic
def update_doctor(request): 
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, instance=request.user.profile)
        if doctor_form.is_valid():
            doctor_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        doctor_form = DoctorForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'doctor_form': doctor_form
    })

@permission_required('update')
@login_required
@transaction.atomic
def update_admin(request): 
    if request.method == 'POST':
        admin_form = AdminForm(request.POST, instance=request.user.profile)
        if admin_form.is_valid():
            admin_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        admin_form = AdminForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'admin_form': admin_form
    })


@permission_required('admit')
@login_required
@transaction.atomic
def admit_patient(request): 
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.patientid)
        patient.admitted = True
        patient.save()
        messages.success(request, _('Patient was successfully admitted!'))
    else:
        messages.error(request, _('Incorrectly formatted request.'))

    return render(request, 'profiles/profile.html')

@permission_required('release')
@login_required
@transaction.atomic
def release_patient(request): 
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.patientid)
        patient.admitted = False
        patient.save()
    else:
        messages.error(request, _('Incorrectly formatted request.'))

    return render(request, 'profiles/profile.html')

@permission_required('transfer')
@login_required
@transaction.atomic
def transfer_patient(request):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=request.patientid)
        patient.hospital = request.hospital
        patient.save()
        messages.success(request, _('Patient was transferred successfully!'))
    else:
        messages.error(request, _('Incorrectly formatted request.'))

    return render(request, 'profiles/profile.html')
