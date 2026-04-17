from .models import Events
from django import forms


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['status', 'type', 'title', 'description', 'date','venue','capacity',
                  'department']
        widgets = {

            'description':forms.Textarea(
              attrs={
                  'class': 'form-control',
              }
            ),
            'venue': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',

            },format='%Y-%m-%dT%H:%M'),
            'department': forms.Select(
                choices=[
                    ('MCA', 'MCA'),
                    ('BCA', 'BCA'),
                    ('BSc CS', 'BSc CS'),
                    ('MSc DS', 'MSc Data Science'),
                    ('All', 'All'),
                ],
                attrs={'class': 'form-select'}
            ),
        }