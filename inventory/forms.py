"""
Forms for inventory management
"""
from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Submit, Row, Column
from crispy_forms.bootstrap import InlineRadios
from decimal import Decimal

from .models import (
    Fornecedor, Produto, CategoriaProduto, NotaFiscal, ItemNotaFiscal,
    Estoque, Movimentacao, AnaliseQualidade, Departamento
)


class FornecedorForm(forms.ModelForm):
    """Form para fornecedor"""
    
    class Meta:
        model = Fornecedor
        fields = [
            'nome_empresa', 'cnpj', 'email_contato', 'telefone',
            'endereco_completo', 'pessoa_contato', 'observacoes', 'ativo'
        ]
        widgets = {
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'email_contato': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'endereco_completo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pessoa_contato': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nome_empresa', css_class='col-md-8'),
                Column('ativo', css_class='col-md-4'),
            ),
            Row(
                Column('cnpj', css_class='col-md-6'),
                Column('pessoa_contato', css_class='col-md-6'),
            ),
            Row(
                Column('email_contato', css_class='col-md-6'),
                Column('telefone', css_class='col-md-6'),
            ),
            'endereco_completo',
            'observacoes',
            Div(
                Submit('submit', 'Salvar Fornecedor', css_class='btn btn-primary'),
                HTML('<a href="{% url "inventory:fornecedores" %}" class="btn btn-secondary ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '').replace('.', '').replace('/', '').replace('-', '')
        if len(cnpj) != 14 or not cnpj.isdigit():
            raise forms.ValidationError('CNPJ deve conter 14 dígitos')
        return cnpj


class ProdutoForm(forms.ModelForm):
    """Form para produto"""
    
    class Meta:
        model = Produto
        fields = [
            'codigo_produto', 'nome_produto', 'categoria', 'descricao',
            'unidade_medida', 'preco_unitario', 'estoque_minimo',
            'requer_analise', 'tempo_analise_dias', 'ativo'
        ]
        widgets = {
            'codigo_produto': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_produto': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unidade_medida': forms.Select(attrs={'class': 'form-select'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'requer_analise': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tempo_analise_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriaProduto.objects.filter(ativo=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('codigo_produto', css_class='col-md-6'),
                Column('categoria', css_class='col-md-6'),
            ),
            'nome_produto',
            'descricao',
            Row(
                Column('unidade_medida', css_class='col-md-4'),
                Column('preco_unitario', css_class='col-md-4'),
                Column('estoque_minimo', css_class='col-md-4'),
            ),
            Row(
                Column('requer_analise', css_class='col-md-6'),
                Column('tempo_analise_dias', css_class='col-md-3'),
                Column('ativo', css_class='col-md-3'),
            ),
            Div(
                Submit('submit', 'Salvar Produto', css_class='btn btn-primary'),
                HTML('<a href="{% url "inventory:produtos" %}" class="btn btn-secondary ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )


class NotaFiscalForm(forms.ModelForm):
    """Form para nota fiscal"""
    
    class Meta:
        model = NotaFiscal
        fields = [
            'numero_nota', 'fornecedor', 'data_emissao', 
            'valor_total', 'observacoes'
        ]
        widgets = {
            'numero_nota': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)
        self.fields['numero_nota'].required = False  # Will be auto-generated
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('numero_nota', css_class='col-md-6'),
                Column('data_emissao', css_class='col-md-6'),
            ),
            Row(
                Column('fornecedor', css_class='col-md-8'),
                Column('valor_total', css_class='col-md-4'),
            ),
            'observacoes',
            HTML('<h5 class="mt-4">Itens da Nota Fiscal</h5>'),
            HTML('<div id="itens-formset">{{ formset }}</div>'),
            Div(
                Submit('submit', 'Salvar Nota Fiscal', css_class='btn btn-primary'),
                HTML('<a href="{% url "inventory:entrada" %}" class="btn btn-secondary ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )


class ItemNotaFiscalForm(forms.ModelForm):
    """Form para item de nota fiscal"""
    
    class Meta:
        model = ItemNotaFiscal
        fields = [
            'produto', 'quantidade', 'valor_unitario', 'lote',
            'data_fabricacao', 'data_validade'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'data_fabricacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('codigo_produto')


# Formset para itens de nota fiscal
ItemNotaFiscalFormSet = inlineformset_factory(
    NotaFiscal, ItemNotaFiscal,
    form=ItemNotaFiscalForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)


class MovimentacaoForm(forms.ModelForm):
    """Form para movimentação de estoque"""
    
    class Meta:
        model = Movimentacao
        fields = [
            'produto', 'estoque', 'tipo_movimentacao', 'quantidade',
            'departamento_origem', 'departamento_destino', 'motivo'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'estoque': forms.Select(attrs={'class': 'form-select'}),
            'tipo_movimentacao': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'departamento_origem': forms.Select(attrs={'class': 'form-select'}),
            'departamento_destino': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('codigo_produto')
        self.fields['estoque'].queryset = Estoque.objects.filter(quantidade__gt=0).select_related('produto')
        self.fields['departamento_origem'].queryset = Departamento.objects.filter(ativo=True)
        self.fields['departamento_destino'].queryset = Departamento.objects.filter(ativo=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('produto', css_class='col-md-6'),
                Column('estoque', css_class='col-md-6'),
            ),
            Row(
                Column('tipo_movimentacao', css_class='col-md-6'),
                Column('quantidade', css_class='col-md-6'),
            ),
            Row(
                Column('departamento_origem', css_class='col-md-6'),
                Column('departamento_destino', css_class='col-md-6'),
            ),
            'motivo',
            Div(
                Submit('submit', 'Registrar Movimentação', css_class='btn btn-primary'),
                HTML('<a href="{% url "inventory:movimentacao" %}" class="btn btn-secondary ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )
    
    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        estoque = cleaned_data.get('estoque')
        quantidade = cleaned_data.get('quantidade')
        
        # Validar se o estoque pertence ao produto selecionado
        if produto and estoque and estoque.produto != produto:
            raise forms.ValidationError('O estoque selecionado não pertence ao produto escolhido.')
        
        # Validar se há quantidade suficiente
        if estoque and quantidade and quantidade > estoque.quantidade:
            raise forms.ValidationError(f'Quantidade insuficiente. Disponível: {estoque.quantidade}')
        
        return cleaned_data


class AnaliseQualidadeForm(forms.ModelForm):
    """Form para análise de qualidade"""
    
    class Meta:
        model = AnaliseQualidade
        fields = ['observacoes']
        widgets = {
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'observacoes',
            Div(
                Submit('submit', 'Iniciar Análise', css_class='btn btn-primary'),
                HTML('<a href="{% url "inventory:analise" %}" class="btn btn-secondary ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )


class FinalizarAnaliseForm(forms.Form):
    """Form para finalizar análise"""
    resultado = forms.ChoiceField(
        choices=AnaliseQualidade.RESULTADO_ANALISE,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    laudo_tecnico = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        required=True,
        label='Laudo Técnico'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'resultado',
            'laudo_tecnico',
            Div(
                Submit('submit', 'Finalizar Análise', css_class='btn btn-success'),
                HTML('<a href="{% url "inventory:analise" %}" class="btn btn-secondary ms-2">Cancelar</a>'),
                css_class='mt-3'
            )
        )


class CategoriaProdutoForm(forms.ModelForm):
    """Form para categoria de produto"""
    
    class Meta:
        model = CategoriaProduto
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartamentoForm(forms.ModelForm):
    """Form para departamento"""
    
    class Meta:
        model = Departamento
        fields = ['nome', 'tipo', 'descricao', 'responsavel', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsavel': forms.Select(attrs={'class': 'form-select'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }