from django import forms
from django.contrib.auth import get_user_model
Users= get_user_model()
class FacultyCreationForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Leave blank for default: faculty@123'
            }
        )
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        )
    )
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','email','department']
        widgets = {
            'first_name' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'

            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'department': forms.Select(
                choices=[
                    ('MCA', 'MCA'),
                    ('BCA', 'BCA'),
                    ('BSc CS', 'BSc CS'),
                    ('MSc DS', 'MSc Data Science'),
                ],
                attrs={'class': 'form-select'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match"
                )
        return cleaned_data

# admin_dashboard/forms.py

class StudentCreationForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Leave blank for default: student@123'
            }
        )
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email',
                  'username', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(
                choices=[
                    ('MCA', 'MCA'),
                    ('BCA', 'BCA'),
                    ('BSc CS', 'BSc CS'),
                    ('MSc DS', 'MSc DS'),
                ],
                attrs={'class': 'form-select'}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match"
                )
        return cleaned_data