from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    re_path(r'.+', views.category, name="category"),
]