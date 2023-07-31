from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("readme", views.readme, name="readme"),
    path("privacy", views.privacy, name="privacy"),
    path("show_detail/SG" + "<sg_id>", views.idv_line, name="details"),
    path("contributions/<username>", views.user_page, name="contributions"),
    path("update_line/SG" + "<sg_id>", views.update_line, name="update_line"),
    path("remove_line/SG" + "<sg_id>", views.remove_line, name="remove_line"),
]