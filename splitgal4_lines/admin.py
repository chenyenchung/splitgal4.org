from django.contrib import admin
from .models import fly_line

@admin.register(fly_line)
class fly_line_admin(admin.ModelAdmin):
    list_display = ('id', 'gene_name', 'effector_type', 'activator_type', 'cassette', 'contributor',)
    ordering = ('id',)
    search_fields = ('gene_name', 'contributor',)
