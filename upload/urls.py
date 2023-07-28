from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("batch_upload", views.upload_file, name="upload"),
    path("add_line", views.add_line, name="add_line"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)