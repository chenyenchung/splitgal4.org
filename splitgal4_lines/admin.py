from django.contrib import admin
from .models import fly_line
from members.models import CustomUser

@admin.register(CustomUser)
class user_admin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'lab',
        'affiliation',
        'is_staff'
    )
    ordering = ('id',)
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'affiliation',
        'lab',
        'verified'
    )

@admin.register(fly_line)    
class fly_line_admin(admin.ModelAdmin):
    list_display = (
        'id',
        'gene_name',
        'effector_type',
        'cassette',
        'contributor',
    )
    ordering = ('id',)
    search_fields = ('gene_name', 'contributor',)
