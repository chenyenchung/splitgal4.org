from django.urls import path
from . import views

urlpatterns = [
    path("user_login", views.user_login, name="login"),
    path("user_logout", views.user_logout, name="logout"),
    path("user_register", views.user_register, name="register"),
    path('send_confirmation', views.activateEmail, name='send_confirmation'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('user_update/<username>', views.user_update, name='user_update'),
    path('pw_update/<username>', views.pw_update, name='pw_update'),
]