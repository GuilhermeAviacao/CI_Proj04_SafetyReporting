from django import forms
from .models import SafetyReport, Comment


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': 'Share your thoughts, insights, or questions about this safety report...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = "Add Comment"
        self.fields['content'].required = True
