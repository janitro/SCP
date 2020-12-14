from django import forms
from web.models import Login, Profesional, Checklist
from .models import Login, Profesional, Checklist

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


class CheckForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CheckForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



















