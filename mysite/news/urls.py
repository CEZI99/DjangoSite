from django.urls import path
from .views import *

urlpatterns = [
      path('', index),
      path('test/', test),
      path('test1/', test1),
      path("test2/", test2),
]