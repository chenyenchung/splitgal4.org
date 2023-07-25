from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("add_line", views.add_line, name="add_line"),
]