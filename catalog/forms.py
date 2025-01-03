from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from .utils import username_validator, validate_password_exists
from django.contrib.auth import authenticate



# В классах SetPasswordMixin и EmailValidator ошибки были переведены на русский
class RegisterForm(UserCreationForm):

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
                    'placeholder': 'Введите пароль',
                    'class': 'register-form-field'
                }
            )
        )
    
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
                    'placeholder':'Повторите пароль',
                    'class': 'register-form-field'
                }
            )
        )

    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
                    'placeholder':'Ваше имя',
                    'class': 'register-form-field'
                }
            )
        )
    
    email = forms.EmailField(
        label='Адрес электронной почты',
        widget=forms.TextInput(attrs={
            'placeholder':'Введите вашу почту',
            'class': 'register-form-field'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваше имя',
            'class': 'login-form-field'
            }
        ),
        validators=[username_validator]
)

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
                'placeholder': 'Введите пароль',
                'class': 'login-form-field'
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(('Логин или пароль не существует'), code='invalid_login' )
                return cleaned_data

class ResetForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
                'placeholder': 'Введите вашу почту',
                'class': 'reset-form-field'
            }
        )
    )
            
