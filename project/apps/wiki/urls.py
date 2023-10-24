from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('edit/', include("apps.wiki.edit.urls")),
    re_path(r".+", views.content, name="content"),
]