from django import forms
from .models import SafetyReport


class SafetyReportForm(forms.ModelForm):
    class Meta:
        model = SafetyReport
        fields = ['place', 'date', 'time', 'description']
        widgets = {
            'place': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location (airport, airspace, etc.)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Provide detailed description of the safety incident or observation...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
