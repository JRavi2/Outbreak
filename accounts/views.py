from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

import requests

from .models import Patient, Hospital, Token
from .forms import UserForm, PatientForm, HospitalForm


def signup_p(request):
    if request.POST:
        userForm = UserForm(request.POST)
        patientForm = PatientForm(request.POST)
        print(userForm.is_valid(), patientForm.is_valid())
        if userForm.is_valid() and patientForm.is_valid():
            # Save User
            userF = userForm.save(commit=False)
            userF.user_type = "P"
            userF.save()
            id = userForm.cleaned_data.get("user_id")
            password = userForm.cleaned_data.get("password")
            user = authenticate(user_id=id, password=password)
            login(request, userF)
            print("Hello")

            # Save Patient
            patient = patientForm.save(commit=False)
            patient.user = userF
            patient.save()
            return redirect("home")
    else:
        userForm = UserForm()
        patientForm = PatientForm()
    return render(
        request,
        "accounts/patient/signUp.html",
        {"userForm": userForm, "patientForm": patientForm},
    )


def signup_h(request):
    if request.POST:
        userForm = UserForm(request.POST)
        hospitalForm = HospitalForm(request.POST)
        print(userForm.is_valid(), hospitalForm.is_valid())
        if userForm.is_valid() and hospitalForm.is_valid():
            # Save User
            user = userForm.save(commit=False)
            user.user_type = "H"
            specialities = hospitalForm.cleaned_data.get("specialities")
            user.save()

            # Save Hospital
            hospital = hospitalForm.save(commit=False)
            hospital.user = user
            # Should use the Geocoding API to get the coordinates
            hospital.latitude = 28.6446
            hospital.longitude = 77.3655
            hospital.save()
            if hospital.hasTokenSystem == False:
                for spec in hospital.specialities:
                    Token.objects.create(user=user, department=spec, count=0)
            return redirect("home")
    else:
        userForm = UserForm()
        hospitalForm = HospitalForm()
    return render(
        request,
        "accounts/hospital/signUp.html",
        {"userForm": userForm, "hospitalForm": hospitalForm},
    )
    pass

@login_required
def goto_dashboard(request):
    if request.user.user_type == "P":
        return redirect('patient_dashboard')
    else:
        return redirect('hospital_dashboard')

@login_required
def patient_dashboard(request):
    user_info = Patient.objects.get(user=request.user)
    return render(request, "accounts/patient/dashboard.html", {"User": user_info})


@login_required
def hospital_dashboard(request):
    user_info = Hospital.objects.get(user=request.user)
    return render(request, "accounts/hospital/dashboard.html", {"User": user_info})


@login_required
def update_tokens(request):
    if request.user.user_type == "H":
        tokens = list(Token.objects.all().filter(user=request.user))
        for t in tokens:
            print(t.count)
        return render(
            request, "accounts/hospital/token-update.html", {"tokens": tokens}
        )


@login_required
def decrease_tokens(request, dept):
    if request.user.user_type == "H":
        token = Token.objects.get(user=request.user, department=dept)
        if token.count > 0:
            token.count = token.count - 1
            token.save()
        return HttpResponse("")
        # redirect('update_tokens')


@login_required
def increase_tokens(request, dept):
    if request.user.user_type == "H":
        token = Token.objects.get(user=request.user, department=dept)
        token.count = token.count + 1
        token.save()
        return HttpResponse("")
        # redirect('update_tokens')
