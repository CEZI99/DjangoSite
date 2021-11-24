from django.urls import path
from .views import *
urlpatterns = [
    path("", CarsHome.as_view(), name='home'),
    path("about", about, name='about'),
    path("add_page", AddPage.as_view(), name='add_page'),
    path("contact", contact, name='contact'),
    path("login", LoginUser.as_view(), name='login'),
    path("logout", logout_user, name='logout'),
    path("register", RegisterUser.as_view(), name='register'),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name='post'),
    path("category/<slug:cat_slug>/", CarsCategory.as_view(), name='category'),
]

hundler404 = pageNotFound
