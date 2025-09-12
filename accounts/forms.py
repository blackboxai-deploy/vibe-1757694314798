"""
Forms for user authentication and management
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class UserLoginForm(forms.Form):
    """
    Formulário de login customizado
    """
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite seu email',
            'required': True
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite sua senha',
            'required': True
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        label='Lembrar de mim',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class UserRegistrationForm(UserCreationForm):
    """
    Formulário de registro customizado
    """
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email',
            'required': True
        })
    )
    
    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome',
            'required': True
        })
    )
    
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu sobrenome',
            'required': True
        })
    )
    
    phone = forms.CharField(
        label='Telefone',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu telefone (opcional)',
            'data-mask': '(00) 00000-0000'
        })
    )
    
    department = forms.CharField(
        label='Departamento',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu departamento (opcional)'
        })
    )
    
    position = forms.CharField(
        label='Cargo',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu cargo (opcional)'
        })
    )
    
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite uma senha forte',
            'required': True
        }),
        help_text='Sua senha deve conter pelo menos 8 caracteres.'
    )
    
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha',
            'required': True
        })
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        label='Aceito os termos de uso e política de privacidade',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        error_messages={
            'required': 'Você deve aceitar os termos de uso para continuar.'
        }
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 
            'phone', 'department', 'position',
            'password1', 'password2'
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove formatting characters
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) not in [10, 11]:  # Brazilian phone formats
                raise ValidationError('Telefone deve ter 10 ou 11 dígitos.')
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Formulário para edição de perfil do usuário
    """
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 
            'phone', 'department', 'position',
            'theme_preference'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone',
                'data-mask': '(00) 00000-0000'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Departamento'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo'
            }),
            'theme_preference': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'phone': 'Telefone',
            'department': 'Departamento',
            'position': 'Cargo',
            'theme_preference': 'Tema Preferido'
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id if self.instance else None
        
        if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError('Este email já está em uso por outro usuário.')
        
        return email


class PasswordChangeForm(forms.Form):
    """
    Formulário para alteração de senha
    """
    current_password = forms.CharField(
        label='Senha Atual',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha atual'
        })
    )
    
    new_password1 = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha'
        }),
        help_text='Sua senha deve conter pelo menos 8 caracteres.'
    )
    
    new_password2 = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError('Senha atual incorreta.')
        return current_password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('As duas senhas não coincidem.')
        
        return password2
    
    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user