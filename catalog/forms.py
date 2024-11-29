from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'register-form-field'
        }))
    
    password_confirm = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={
        'placeholder':'Повторите пароль',
        'class': 'register-form-field'
        }))
    
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'placeholder':'Ваше имя',
        'class': 'register-form-field'
        }))
    
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.TextInput(attrs={
        'placeholder':'Введите вашу почту',
        'class': 'register-form-field'
        }))
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'placeholder': 'Введите ваше имя',
        'class': 'login-form-field'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'login-form-field'
    }))

class ResetForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        'placeholder': 'Введите вашу почту',
        'class': 'reset-form-field'
    }))
