from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3  # Пагинация страницы, по 3 поста на страницу

    def get_user_context(self, **kwargs):  # Создает контекст для шаблона
        context = kwargs  # Для передачи аргументов из views.py
        cats = Category.objects.annotate(Count('cars'))  # Количество постов связянных с этой рубрикой
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:  # Если пользователь не авторизован, то удаляем 1 из menu
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
