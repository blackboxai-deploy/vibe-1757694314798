"""
Views for user authentication and management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import CustomUser, UserPermission
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .utils import log_user_activity, has_permission


def login_view(request):
    """
    View para login de usuários
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserLoginForm()
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_active:
                    if user.is_email_verified:
                        login(request, user)
                        log_user_activity(request, user, 'Login realizado')
                        
                        # Redirect to next page or dashboard
                        next_page = request.GET.get('next', 'dashboard')
                        messages.success(request, f'Bem-vindo, {user.get_full_name()}!')
                        return redirect(next_page)
                    else:
                        messages.error(
                            request, 
                            'Seu email ainda não foi verificado. Verifique sua caixa de entrada.'
                        )
                else:
                    messages.error(request, 'Sua conta está desativada.')
            else:
                messages.error(request, 'Email ou senha incorretos.')
    
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """
    View para registro de novos usuários
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # User is active but needs email verification
            user.is_email_verified = False
            user.save()
            
            # Send verification email
            send_verification_email(request, user)
            
            messages.success(
                request,
                'Conta criada com sucesso! Verifique seu email para ativar sua conta.'
            )
            return redirect('accounts:login')
    
    return render(request, 'accounts/register.html', {'form': form})


def send_verification_email(request, user):
    """
    Envia email de verificação para o usuário
    """
    subject = 'Verificação de Email - Sistema de Estoque'
    
    # Create verification link
    verification_link = request.build_absolute_uri(
        reverse('accounts:verify_email', args=[user.email_verification_token])
    )
    
    message = render_to_string('accounts/email/verification.html', {
        'user': user,
        'verification_link': verification_link,
        'company_name': settings.COMPANY_NAME,
    })
    
    send_mail(
        subject,
        '',  # Plain text message (empty since we're using HTML)
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
        fail_silently=False,
    )


def verify_email(request, token):
    """
    View para verificação de email
    """
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
            
            log_user_activity(request, user, 'Email verificado')
            
            messages.success(
                request,
                'Email verificado com sucesso! Você já pode fazer login.'
            )
        else:
            messages.info(request, 'Este email já foi verificado anteriormente.')
            
    except CustomUser.DoesNotExist:
        messages.error(request, 'Token de verificação inválido.')
    
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """
    Dashboard principal do sistema
    """
    # Import here to avoid circular imports
    from inventory.models import Produto, Estoque, Movimentacao
    from datetime import datetime, timedelta
    
    # Basic statistics
    total_products = Produto.objects.count()
    total_stock_items = Estoque.objects.filter(quantidade__gt=0).count()
    recent_movements = Movimentacao.objects.select_related(
        'produto', 'usuario'
    ).order_by('-data_movimentacao')[:10]
    
    # Products expiring soon (next 30 days)
    expiring_soon = Estoque.objects.filter(
        data_validade__lte=datetime.now().date() + timedelta(days=30),
        quantidade__gt=0
    ).select_related('produto').order_by('data_validade')[:10]
    
    # Low stock alerts (assuming minimum stock level of 10)
    low_stock = Estoque.objects.filter(
        quantidade__lte=10,
        quantidade__gt=0
    ).select_related('produto').order_by('quantidade')[:10]
    
    context = {
        'total_products': total_products,
        'total_stock_items': total_stock_items,
        'recent_movements': recent_movements,
        'expiring_soon': expiring_soon,
        'low_stock': low_stock,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def profile_view(request):
    """
    View para visualização e edição do perfil do usuário
    """
    form = UserProfileForm(instance=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            log_user_activity(request, request.user, 'Perfil atualizado')
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    
    context = {
        'form': form,
        'user_permissions': UserPermission.objects.filter(
            user=request.user, 
            is_active=True
        ).select_related(),
    }
    
    return render(request, 'accounts/profile.html', context)


@require_POST
@csrf_protect
def toggle_theme(request):
    """
    Ajax view para alternar tema do usuário
    """
    if request.user.is_authenticated:
        theme = request.POST.get('theme')
        if theme in ['light', 'dark', 'auto']:
            request.user.theme_preference = theme
            request.user.save()
            
            log_user_activity(request, request.user, f'Tema alterado para {theme}')
            
            return JsonResponse({'success': True, 'theme': theme})
    
    return JsonResponse({'success': False})


@login_required
def logout_view(request):
    """
    View para logout do usuário
    """
    user = request.user
    log_user_activity(request, user, 'Logout realizado')
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('accounts:login')