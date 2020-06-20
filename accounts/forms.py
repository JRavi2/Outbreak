from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Hospital


class UserForm (UserCreationForm):
    user_id = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = {'user_id', 'password1', 'password2'}


class PatientForm (forms.ModelForm):

    class Meta:
        model = Patient
        fields = {'name', 'age', 'gender',
                  'contact_no', 'social_status', 'prefd_hospital'}

class HospitalForm (forms.ModelForm):

    class Meta:
        model = Hospital
        fields = {'name', 'address', 'bed_capacity', 'currently_free', 'hasTokenSystem', 'linkToTokenWebsite', 'specialities'}
