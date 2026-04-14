from django import forms
from .models import Resource
from django.core.validators import FileExtensionValidator
class ResourceForm(forms.ModelForm):
    file_upload = forms.FileField(
        label="Upload Resource",
        help_text="Allowed format: PDF only.",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control','accept': '.pdf'}))
    class Meta:
        model = Resource
        fields = ['title', 'description', 'subject', 'category', 'department']
        widgets ={
        'title': forms.TextInput(
            attrs={
                'class': 'form-control',

            }),
        }
