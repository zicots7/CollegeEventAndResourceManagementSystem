from .models import Registration
from django import forms

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []
