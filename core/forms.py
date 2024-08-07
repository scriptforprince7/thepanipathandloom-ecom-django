from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class ExportCartOrdersForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    paid_status = forms.ChoiceField(
        choices=[
            ('', 'All'),  # Allowing all options
            ('True', 'Paid'),
            ('False', 'Unpaid')
        ],
        required=False
    )