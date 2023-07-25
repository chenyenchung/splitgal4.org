from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("batch_upload", views.upload_file, name="upload"),
    path("add_new", views.create_new_line, name="add_new"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)