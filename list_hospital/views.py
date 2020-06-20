from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .APIs import find_place, check
from accounts.models import Patient
from .chatbot import *
import json
import time


def search(request):
    if request.POST:
        return redirect("list_hospitals", {"data": request.POST["data"]})
    else:
        return render(request, "list_hospitals/search.html", {})


def list_hospitals(request, disease):
    if disease:
        # Generate all nearby facilities'
        # print(request.GET)
        print(str(disease).strip())
        hospitals = check(str(disease), 28.630999, 77.372165)
    else:
        # Generate Customised facilities
        hospitals = find_place(28.6358749, 77.3738937, ["clinic"])
    return render(request, "list_hospitals/index.html", {"hospitals": hospitals})
