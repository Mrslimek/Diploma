from django.contrib.auth.models import User
from django.forms import ValidationError
from django.contrib.auth import authenticate

def username_validator(value):
    if not User.objects.filter(username=value).exists():
        print('Работает username_validator')
        raise ValidationError('Логин или пароль не действительны.')
    
def validate_password_exists(password, username):
    user = authenticate(username=username, password=password)
    if user is None:
        print('Работает password validator')
        raise ValidationError('Логин или пароль не существует')