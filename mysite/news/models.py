from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_content = models.DateTimeField(auto_now_add=True)
    updated_content = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="Изображения/Y%/m%/%d")
    mb_published = models.BooleanField(default=True)