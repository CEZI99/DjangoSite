from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


cats = Category.objects.all()
posts = Cars.objects.all()
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def start_page(request):
    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        "title": "Главная страница.",
        "cat_selected": 0,
    }
    return render(request, "cars/start_page.html", context=context)


def about(request):
    return render(request, "cars/about.html", {"title": "О сайте."})


def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            #  print(form.cleaned_data)
            try:
                Cars.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, "Ошибка добавления поста")
    else:
        form = AddPostForm()
    return render(request, "cars/addpage.html", {'form': form, "menu": menu, "title": "Добавление статьи"})


def contact(request):
    return HttpResponse("<h1>Page</h1>")


def login(request):
    return HttpResponse("<h1>Page</h1>")


def show_post(request, post_slug):
    post = get_object_or_404(Cars, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'cars/post.html', context=context)


def show_category(request, cat_id):
    posts = Cars.objects.filter(cat_id=cat_id)

    #if len(posts) == 0:
        #raise Http404()

    context = {
        "posts": posts,
        "title": "Отображение по рубрикам.",
        "cat_selected": cat_id,
    }
    return render(request, "cars/start_page.html", context=context)


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
