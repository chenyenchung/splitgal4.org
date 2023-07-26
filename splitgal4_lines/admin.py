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
    # Only allow staff to see what they upload
    def get_queryset (self, request):
        if not request.user.is_superuser:
            return fly_line.objects.filter(uploader= request.user)
        return fly_line.objects.all()
    
    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    # Only allow staff to change what they upload
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.uploader != request.user.username:
            return False
        return True
    def change_view(self, request, object_id, extra_context=None):
        if not request.user.is_superuser:      
            self.exclude = ('need_review', 'date_created', 'uploader')
        return super(fly_line_admin, self).change_view(request, object_id, extra_context)

    list_display = (
        'id',
        'gene_name',
        'effector_type',
        'cassette',
        'contributor',
    )
    ordering = ('id',)
    search_fields = ('gene_name', 'contributor',)
