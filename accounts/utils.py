"""
Utility functions for accounts app
"""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import UserPermission, UserActivity
from functools import wraps


def log_user_activity(request, user, action, description=''):
    """
    Registra atividade do usuário no sistema
    """
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Get user agent
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
    
    UserActivity.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent
    )


def has_permission(user, module, permission):
    """
    Verifica se o usuário tem uma permissão específica
    """
    if not user.is_authenticated:
        return False
    
    # Superuser has all permissions
    if user.is_superuser:
        return True
    
    # Check specific permission
    return UserPermission.objects.filter(
        user=user,
        module=module,
        permission=permission,
        is_active=True
    ).exists()


def permission_required(module, permission, raise_exception=False):
    """
    Decorator para verificar permissões específicas
    """
    def check_permission(user):
        return has_permission(user, module, permission)
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            
            if not check_permission(request.user):
                if raise_exception:
                    return HttpResponseForbidden(
                        "Você não tem permissão para acessar esta página."
                    )
                else:
                    return render(request, 'errors/403.html', status=403)
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def get_user_permissions(user):
    """
    Retorna todas as permissões do usuário organizadas por módulo
    """
    if not user.is_authenticated:
        return {}
    
    if user.is_superuser:
        # Superuser has all permissions
        from .models import UserPermission
        modules = dict(UserPermission.MODULE_CHOICES)
        permissions = dict(UserPermission.PERMISSION_CHOICES)
        
        result = {}
        for module_key, module_name in modules.items():
            result[module_key] = {
                'name': module_name,
                'permissions': list(permissions.keys())
            }
        return result
    
    # Get user specific permissions
    user_permissions = UserPermission.objects.filter(
        user=user,
        is_active=True
    ).values('module', 'permission')
    
    # Organize by module
    result = {}
    for perm in user_permissions:
        module = perm['module']
        permission = perm['permission']
        
        if module not in result:
            result[module] = {
                'name': dict(UserPermission.MODULE_CHOICES).get(module, module),
                'permissions': []
            }
        
        result[module]['permissions'].append(permission)
    
    return result


def can_access_module(user, module):
    """
    Verifica se o usuário pode acessar um módulo (tem pelo menos uma permissão)
    """
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    return UserPermission.objects.filter(
        user=user,
        module=module,
        is_active=True
    ).exists()


def get_navigation_items(user):
    """
    Retorna os itens de navegação baseados nas permissões do usuário
    """
    if not user.is_authenticated:
        return []
    
    navigation_items = []
    
    # Dashboard - always available for authenticated users
    navigation_items.append({
        'name': 'Dashboard',
        'url': 'dashboard',
        'icon': 'fas fa-tachometer-alt',
        'active': True
    })
    
    # Define navigation based on permissions
    nav_config = [
        {
            'name': 'Entrada',
            'url': 'inventory:entrada',
            'icon': 'fas fa-arrow-down',
            'module': 'entrada',
            'permission': 'view'
        },
        {
            'name': 'Movimentação',
            'url': 'inventory:movimentacao',
            'icon': 'fas fa-exchange-alt',
            'module': 'movimentacao',
            'permission': 'view'
        },
        {
            'name': 'Análise',
            'url': 'inventory:analise',
            'icon': 'fas fa-microscope',
            'module': 'analise',
            'permission': 'view'
        },
        {
            'name': 'Fornecedores',
            'url': 'inventory:fornecedores',
            'icon': 'fas fa-truck',
            'module': 'fornecedores',
            'permission': 'view'
        },
        {
            'name': 'Produtos',
            'url': 'inventory:produtos',
            'icon': 'fas fa-boxes',
            'module': 'produtos',
            'permission': 'view'
        },
        {
            'name': 'Relatórios',
            'url': 'analytics:relatorios',
            'icon': 'fas fa-chart-bar',
            'module': 'relatorios',
            'permission': 'view'
        },
        {
            'name': 'Configurações',
            'url': 'accounts:configuracoes',
            'icon': 'fas fa-cog',
            'module': 'configuracoes',
            'permission': 'view'
        },
    ]
    
    # Add items based on user permissions
    for item in nav_config:
        if has_permission(user, item['module'], item['permission']):
            navigation_items.append({
                'name': item['name'],
                'url': item['url'],
                'icon': item['icon'],
                'active': True
            })
    
    return navigation_items


def get_user_theme(request):
    """
    Retorna o tema preferido do usuário
    """
    if request.user.is_authenticated:
        return request.user.theme_preference
    return 'auto'


class PermissionMixin:
    """
    Mixin para views que requerem permissões específicas
    """
    required_permission = None
    required_module = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        
        if self.required_module and self.required_permission:
            if not has_permission(request.user, self.required_module, self.required_permission):
                return render(request, 'errors/403.html', status=403)
        
        return super().dispatch(request, *args, **kwargs)