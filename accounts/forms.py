#Django
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
#project
from .utils import *
from .models import *


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


class CustomUserChangeForm(forms.ModelForm):
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={
        'class': 'input_field',
        'placeholder': 'Введите пароль'
    }), required=False)
    password2 = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={
        'class': 'input_field',
        'placeholder': 'Подтвердите пароль'
    }), required=False)
    first_name = forms.CharField(label='имя', widget=forms.TextInput(attrs={
        'class': 'input_field'
    }), required=False)
    last_name = forms.CharField(label='фамилия', widget=forms.TextInput(attrs={
        'class': 'input_field'
    }), required=False)
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.TextInput(attrs={
        'class': 'input_field'
    }), required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
    
    def save(self):
        print('РАБОТАЕТ SAVE')
        print(self.cleaned_data.items(), 'CLEANED DATA ITEMS')

        instance = self.instance

        for key, value in self.cleaned_data.items():
            if key == 'password1' and value:
                instance.set_password(value)
            else: 
                if value:
                    print(f'добавил atr - {value}')
                    setattr(instance, key, value)

        return instance


class UserProfileChangeForm(forms.ModelForm):
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={
        'class': 'input_field'
    }), required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.TextInput(attrs={
        'class': 'input_field',
        'type': 'date'
    }), required=False)
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth']
        