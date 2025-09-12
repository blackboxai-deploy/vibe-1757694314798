"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, UserPermission, UserRole, UserActivity


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin customizado para CustomUser
    """
    list_display = [
        'email', 'first_name', 'last_name', 'department', 
        'position', 'is_email_verified', 'is_active', 'created_at'
    ]
    
    list_filter = [
        'is_active', 'is_email_verified', 'is_staff', 
        'is_superuser', 'department', 'theme_preference', 'created_at'
    ]
    
    search_fields = [
        'email', 'first_name', 'last_name', 
        'username', 'department', 'position'
    ]
    
    readonly_fields = [
        'email_verification_token', 'created_at', 'updated_at', 
        'last_login', 'date_joined'
    ]
    
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'phone', 'department', 'position'
            )
        }),
        ('Permissões', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Configurações da Conta', {
            'fields': (
                'is_email_verified', 'email_verification_token',
                'theme_preference'
            )
        }),
        ('Informações de Auditoria', {
            'fields': (
                'last_login', 'date_joined', 
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    add_fieldsets = (
        ('Informações Básicas', {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2'
            ),
        }),
        ('Informações Adicionais', {
            'fields': (
                'phone', 'department', 'position',
                'is_active', 'is_email_verified'
            )
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


class UserPermissionInline(admin.TabularInline):
    """
    Inline para permissões do usuário
    """
    model = UserPermission
    fk_name = 'user'
    extra = 1
    fields = ['module', 'permission', 'is_active', 'granted_at']
    readonly_fields = ['granted_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('granted_by')


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """
    Admin para gerenciamento de permissões
    """
    list_display = [
        'user', 'get_user_email', 'module', 'permission', 
        'is_active', 'granted_by', 'granted_at'
    ]
    
    list_filter = [
        'module', 'permission', 'is_active', 'granted_at'
    ]
    
    search_fields = [
        'user__first_name', 'user__last_name', 
        'user__email', 'user__username'
    ]
    
    readonly_fields = ['granted_at']
    
    ordering = ['-granted_at']
    
    raw_id_fields = ['user', 'granted_by']
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email do Usuário'
    get_user_email.admin_order_field = 'user__email'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new permission
            obj.granted_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'granted_by'
        )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Admin para gerenciamento de funções
    """
    list_display = [
        'name', 'description', 'get_users_count', 
        'is_active', 'created_at'
    ]
    
    list_filter = ['is_active', 'created_at']
    
    search_fields = ['name', 'description']
    
    filter_horizontal = ['users']
    
    readonly_fields = ['created_at']
    
    def get_users_count(self, obj):
        return obj.users.count()
    get_users_count.short_description = 'Qtd. Usuários'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('users')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Admin para visualização de atividades dos usuários
    """
    list_display = [
        'user', 'get_user_email', 'action', 
        'ip_address', 'timestamp'
    ]
    
    list_filter = [
        'action', 'timestamp', 'user__department'
    ]
    
    search_fields = [
        'user__first_name', 'user__last_name',
        'user__email', 'action', 'description'
    ]
    
    readonly_fields = [
        'user', 'action', 'description', 
        'ip_address', 'user_agent', 'timestamp'
    ]
    
    ordering = ['-timestamp']
    
    date_hierarchy = 'timestamp'
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'
    get_user_email.admin_order_field = 'user__email'
    
    def has_add_permission(self, request):
        return False  # Activity logs are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Activity logs should not be modified
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# Customize User admin to include permissions inline
CustomUserAdmin.inlines = [UserPermissionInline]