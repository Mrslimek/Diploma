from django.shortcuts import render
from django.views.generic import CreateView
from .forms import RegisterForm, LoginForm, ResetForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    return render(request, 'Zoo.html')

def catalog(request):
    return render(request, 'catalogZoo.html')

def card_product(request):
    return render(request, 'cardProduct.html')

def brands(request):
    return render(request, 'brands.html')

def basket(request):
    return render(request, 'basket.html')

def articles(request):
    return render(request, 'articles.html')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login/')

    def form_valid(self, form):
        # Создаем пользователя
        user = form.save(commit=False)  # Не сохраняем сразу
        user.set_password(form.cleaned_data['password'])  # Устанавливаем зашифрованный пароль
        user.save()  # Сохраняем пользователя в базе данных

        return super().form_valid(form)  # Возвращаем результат родительского метода

    def form_invalid(self, form):
        # Если форма невалидна, возвращаем стандартный ответ
        return super().form_invalid(form)

def login(request):

    form = LoginForm()

    if request.method == 'POST':
        form_data = LoginForm(data=request.POST)
        

    return render(request, 'login.html', {'form': form})

def reset_password(request):

    form = ResetForm()

    if request.method == 'POST':
        form_data = ResetForm(request.POST)

    return render(request, 'reset_form.html', {'form': form})
