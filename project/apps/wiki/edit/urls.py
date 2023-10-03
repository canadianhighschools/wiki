from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('browse', views.browse, name="browse"),
    path('category/<int:pk>', views.category, name="category"),
]