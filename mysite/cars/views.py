from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from .forms import *

cats = Category.objects.all()
posts = Cars.objects.all()
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class CarsHome(ListView):
    model = Cars  # Выбирает все записи модели Cars и отображает в виде списка
    template_name = 'cars/start_page.html'  # Указываем путь к шаблону
    context_object_name = 'posts'  # Указываем переменную posts для шаблона start_page.html

    def get_context_data(self, *, object_list=None, **kwargs):
        # Функция формирования динамических и статических контекста и передает в шаблон
        context = super().get_context_data(**kwargs)
        # Обращаемся к базовому классу ListView и взять у него существующий контекст
        context['menu'] = menu
        # Дбавляем перменную menu для шаблона start_page.html
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Cars.objects.filter(mb_published=True)


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


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'cars/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context

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


def login(request):
    return HttpResponse("<h1>Page</h1>")


class ShowPost(DetailView):
    model = Cars
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug'  # Подставляем пересменную post_slug в маршрутизацию
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


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


class CarsCategory(ListView):
    model = Category
    template_name = 'cars/start_page.html'
    context_object_name = 'posts'
    allow_empty = False  # Для исключения 404

    def get_queryset(self):
        # Выбираем записи из таблицы Cars только те, которым соответствует категория по указанному слагу
        return Cars.objects.filter(cat__slug=self.kwargs['cat_slug'], mb_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # Берем первую запись из posts и обращаемся к параметру атрибуту cat, который возвращает название категории
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context


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


def bmw(request):
    series = CarsSeries.objects.all()
    return render(request, "cars/bmw.html", {"series": series, "title": "BMW"})


def mercedes(request):
    series = CarsSeries.objects.all()
    return render(request, "cars/mercedes.html", {"series": series, "title": "Mercedes"})


def porsche(request):
    series = CarsSeries.objects.all()
    return render(request, "cars/porsche.html", {"series": series, "title": "Porsche"})


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
