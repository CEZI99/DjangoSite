from django import forms
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
