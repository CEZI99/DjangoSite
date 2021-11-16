from django.contrib import admin

from .models import *


class CarsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo_cars', 'created_content', 'mb_published')  # Дополнительные поля в админке
    list_display_links = ('id', 'title')  # Содержит те поля на которые сможем кликнуть
    search_fields = ('title', 'content')  # По каким полям можно осуществлять поиск
    list_editable = ('mb_published',)  # Позволяет редактирвание mb_published
    list_filter = ('mb_published', 'created_content')  # Фильтры по публикациям и по дате создания
    prepopulated_fields = {"slug": ("title",)}  # Повторяет slug в поле URL


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}  # Повторяет slug в поле URL


admin.site.register(Cars, CarsAdmin)
admin.site.register(Category, CategoryAdmin)
