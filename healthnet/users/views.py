from django.shortcuts import render
from django.contrib.auth import authenticate, login

# Create your views here.

@permission_required('update_patient')
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = PersonForm(request.POST, instance=request.user)
        profile_form = PatientForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = PersonForm(instance=request.user)
        profile_form = PatientForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'patient_form': user_form,
        'profile_form': profile_form
    })

@permission_required('signup')
@login_required
@transaction.atomic
def signup_patient(request): 
    if request.method == 'POST':
        user_form = PersonForm(request.POST, instance=request.user)
        patient_form = PatientForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            patient_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = PersonForm(instance=request.user)
        patient_form = PatientForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'patient_form': person_form,
        'profile_form': patient_form
    })

@permission_required('update')
@login_required
@transaction.atomic
def update_nurse(request): 
    if request.method == 'POST':
        user_form = PersonForm(request.POST, instance=request.user)
        nurse_form = NurseForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            nurse_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = PersonForm(instance=request.user)
        nurse_form = NurseForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'patient_form': person_form,
        'nurse_form': nurse_form
    })

@permission_required('update')
@login_required
@transaction.atomic
def update_doctor(request): 
    if request.method == 'POST':
        user_form = PersonForm(request.POST, instance=request.user)
        doctor_form = DoctorForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            doctor_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = PersonForm(instance=request.user)
        doctor_form = DoctorForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'patient_form': person_form,
        'doctor_form': doctor_form
    })

@permission_required('update')
@login_required
@transaction.atomic
def update_admin(request): 
    if request.method == 'POST':
        user_form = PersonForm(request.POST, instance=request.user)
        admin_form = AdminForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            admin_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = PersonForm(instance=request.user)
        admin_form = AdminForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'patient_form': person_form,
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
