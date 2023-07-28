from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("readme", views.readme, name="readme"),
    path("privacy", views.privacy, name="privacy"),
]