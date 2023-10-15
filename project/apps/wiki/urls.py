from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    re_path(r'edit/.+', views.edit, name="edit"),
    re_path(r".+", views.content, name="content"),
]