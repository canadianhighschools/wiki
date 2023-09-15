from django.urls import path, re_path

from . import views

urlpatterns = [
    # wiki api
    path(r"wiki/.+", views.content, name="content"),
]