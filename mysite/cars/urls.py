from django.urls import path
from .views import *
urlpatterns = [
    path("", start_page, name='home'),
    path("about", about, name='about'),
    path("add_page", add_page, name='add_page'),
    path("contact", contact, name='contact'),
    path("login", login, name='login'),
    path("post/<int:post_id>/", show_post, name='post'),
    path("category/<int:cat_id>/", show_category, name='category'),
    path("bmw/", bmw),
    path("mercedes/", mercedes),
    path("porsche/", porsche),

]

hundler404 = pageNotFound