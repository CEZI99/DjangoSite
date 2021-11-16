from django.db import models
from django.urls import reverse


class Cars(models.Model):
    title = models.CharField(max_length=100, verbose_name="Загаловок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo_cars = models.ImageField(upload_to="Изображения/Y%/m%/%d", verbose_name="Фото")
    car_info = models.TextField(blank=True, verbose_name="Информация")
    created_content = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_content = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    mb_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Функция динамическая ссылка
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        """Замена модели Cars на русскоязычное слово Автомобили, сортировка"""
        verbose_name = "марку автомобиля"
        verbose_name_plural = "Автомобили"
        ordering = ["created_content", "title"]


class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = "категорию"
        verbose_name_plural = "Категории"
        ordering = ["id"]
