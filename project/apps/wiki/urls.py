from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    # path('edit', views.index, name="edit"),
    re_path(r".+", views.content, name="content"),
]