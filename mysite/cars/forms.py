from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # Вызываем конструктор при добавлении поста
        super().__init__(*args, **kwargs)  # Обращаемся к родительскому классу
        self.fields['cat'].empty_label = "Категория не выбрана"  # У родительского класса меняем поле 'cat'

    class Meta:
        model = Cars
        fields = ['title', 'slug', 'car_info', 'photo_cars', 'mb_published', 'cat']
        widgets = {  # Определение стилей
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'car_info': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):  # Валидатор для записи title в модели Cars
        title = self.cleaned_data['title']
        if len(title) > 20:
            raise ValidationError('Длина превышает 20 символов')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
    captcha = CaptchaField(label="Докажите, что вы не робот")
