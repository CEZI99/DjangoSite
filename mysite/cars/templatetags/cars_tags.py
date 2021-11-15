from django import template
from cars.models import *

register = template.Library()
cats = Category.objects.all()
posts = Cars.objects.all()
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


@register.simple_tag(name='get_cats')
def get_categories(filter=None):  # simple_tag, простой тег
    if not filter:
        return cats
    else:
        return Category.objects.filter(pk=filter)


@register.simple_tag(name='get_posts')
def get_posts():
    return posts


@register.simple_tag(name='get_menu')
def get_menu():
    return menu


@register.inclusion_tag('cars/list_categories.html')
def show_categories(sort=None, cat_selected=0):  # inclusion_tag, Включающий тег
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected}
