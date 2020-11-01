from django import forms
from web.models import Login, Profesional

class loginForm(forms.Form):
    email= forms.EmailField(
        label='email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'email',
                'class':'form-control',
            }
        )
    )
    password = forms.CharField(
        label='password',
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'password',
                'class':'form-control',
            }
        )
    )



