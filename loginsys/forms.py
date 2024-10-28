from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from django.forms import EmailField, PasswordInput, CharField, TextInput

from loginsys.models import Profiles


class LoginForm(forms.Form):
    email = EmailField(label='Почта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}), required=True,
                         initial='Пароль')
    captcha = ReCaptchaField(public_key='6LetcloqAAAAAGv3GLPj8_I7hP1WJQC1w5A8cuiW',
                             private_key='6LetcloqAAAAADL_JYTwWhEg9-oN1GubFXWxrkKF', widget=ReCaptchaV3())


class RegisterForm(forms.Form):
    name = CharField(label='Имя', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = EmailField(label='Почта', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}), required=True,
                         initial='Пароль')
    confirm_password = CharField(label='Потверждение пароля', widget=PasswordInput(attrs={'class': 'form-control'}),
                                 required=True,
                                 initial='Потверждение пароля')
    captcha = ReCaptchaField(public_key='6LetcloqAAAAAGv3GLPj8_I7hP1WJQC1w5A8cuiW',
                             private_key='6LetcloqAAAAADL_JYTwWhEg9-oN1GubFXWxrkKF', widget=ReCaptchaV3())


class ProfileForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Profiles
        fields = ['photo', 'birthdate']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        return cleaned_data


class UserForm(forms.ModelForm):
    first_name = CharField(label='Имя', widget=TextInput(attrs={'class': 'form-control'}), required=True,
                           initial='Имя')

    class Meta:
        model = User
        fields = ['first_name']
