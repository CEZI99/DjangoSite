from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *


class CarsHome(DataMixin, ListView):
    model = Cars  # Выбирает все записи модели Cars и отображает в виде списка
    template_name = 'cars/start_page.html'  # Указываем путь к шаблону
    context_object_name = 'posts'  # Указываем переменную posts для шаблона start_page.html

    def get_context_data(self, *, object_list=None, **kwargs):
        # Функция формирования динамических и статических контекста и передает в шаблон
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница.')  # Можем обращаться ко всем методам базового класса

        return dict(list(context.items()) + list(c_def.items()))  # Обьеденение списков в словарь context

    def get_queryset(self):  # Выборка записей из таблицы Cars
        return Cars.objects.filter(mb_published=True).select_related('cat')  # Убираем дубли в SQL заросах
        # Реализует "жадный" запрос, берёт все связанные данные из модели Category и тогда при выводе рубрик
        # в base.html не будет выполнятся дополнительный  SQL запрос


# """Замена на классы представления"""
# def start_page(request):
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         "title": "Главная страница.",
#         "cat_selected": 0,
#     }
#     return render(request, "cars/start_page.html", context=context)


def about(request):
    return render(request, "cars/about.html", {"title": "О сайте."})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cars/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')  # Можем обращаться ко всем методам базового класса

        return dict(list(context.items()) + list(c_def.items()))  # Обьеденение списков в словарь context


# """Замена на классы представления"""
# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, "cars/addpage.html", {'form': form, "menu": menu, "title": "Добавление статьи"})


def contact(request):
    return HttpResponse("<h1>Page</h1>")


# def login(request):
#     return HttpResponse("<h1>Page</h1>")


class ShowPost(DataMixin, DetailView):
    model = Cars
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'  # Подставляем пересменную post_slug в маршрутизацию
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='post')  # Можем обращаться ко всем методам базового класса

        return dict(list(context.items()) + list(c_def.items()))  # Обьеденение списков в словарь context


# """Замена на классы представления"""
# def show_post(request, post_slug):
#     post = get_object_or_404(Cars, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'cars/post.html', context=context)


class CarsCategory(DataMixin, ListView):
    model = Category
    template_name = 'cars/start_page.html'
    context_object_name = 'posts'
    allow_empty = False  # Для исключения 404

    def get_queryset(self):
        # Выбираем записи из таблицы Cars только те, которым соответствует категория по указанному слагу
        return Cars.objects.filter(cat__slug=self.kwargs['cat_slug'], mb_published=True).select_related('cat')
        # Убираем дубли в SQL заросах
        # Реализует "жадный" запрос, берёт все связанные данные из модели Category и тогда при выводе рубрик
        # в base.html не будет выполнятся дополнительный  SQL запрос

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])  # Оптимизация вложенного запрса, удаления дублей(SQL)
        c_def = self.get_user_context(title="Категория - " + str(c.name),
                                      cat_selected=c.pk)
        # Берем первую запись из posts и обращаемся к параметру атрибуту cat, который возвращает название категории
        return dict(list(context.items()) + list(c_def.items()))  # Обьеденение списков в словарь context


# """Замена на классы представления"""
# def show_category(request, cat_id):
#     posts = Cars.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#     raise Http404()
#
#     context = {
#         "posts": posts,
#         "title": "Отображение по рубрикам.",
#         "cat_selected": cat_id,
#     }
#     return render(request, "cars/start_page.html", context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "cars/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')  # Можем обращаться ко всем методам базового класса

        return dict(list(context.items()) + list(c_def.items()))  # Обьеденение списков в словарь context

    def form_valid(self, form):  # Метод вызывается при успешной формы регистрации
        user = form.save()  # Сохранение формы в БД
        login(self.request, user)  # Функция, которая сразу же авторизовывает пользователя
        return redirect('home')  # После авторизации возвращаемся домой


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "cars/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')  # Можем обращаться ко всем методам базового класса

        return dict(list(context.items()) + list(c_def.items()))  # Обьеденение списков в словарь context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):  # Функция представления для выхода пользователю из авторизации
    logout(request)
    return redirect("login")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
