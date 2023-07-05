from django.urls import path
from . import views

urlpatterns = [
    path("user_login", views.user_login, name="login"),
    path("user_logout", views.user_logout, name="logout"),
    path("user_register", views.user_register, name="register"),
]