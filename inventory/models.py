"""
Models for inventory management system
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from datetime import datetime, timedelta

User = get_user_model()


class Departamento(models.Model):
    """
    Modelo para departamentos da empresa
    """
    TIPOS_DEPARTAMENTO = [
        ('analise', 'DEP. Análise'),
        ('laboratorio', 'DEP. Laboratório'),
        ('industrial', 'DEP. Industrial'),
        ('estoque', 'DEP. Estoque'),
        ('expedicao', 'DEP. Expedição'),
    ]
    
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Departamento"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_DEPARTAMENTO,
        verbose_name="Tipo"
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departamentos_responsavel',
        verbose_name="Responsável"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    """
    Modelo para fornecedores
    """
    nome_empresa = models.CharField(
        max_length=200,
        verbose_name="Nome da Empresa"
    )
    
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )
    
    email_contato = models.EmailField(
        verbose_name="Email de Contato"
    )
    
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone"
    )
    
    endereco_completo = models.TextField(
        verbose_name="Endereço Completo"
    )
    
    pessoa_contato = models.CharField(
        max_length=200,
        verbose_name="Pessoa de Contato"
    )
    
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome_empresa']
    
    def __str__(self):
        return f"{self.nome_empresa} ({self.cnpj})"


class CategoriaProduto(models.Model):
    """
    Modelo para categorias de produtos
    """
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da Categoria"
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Produto(models.Model):
    """
    Modelo para produtos
    """
    codigo_produto = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código do Produto"
    )
    
    nome_produto = models.CharField(
        max_length=200,
        verbose_name="Nome do Produto"
    )
    
    categoria = models.ForeignKey(
        CategoriaProduto,
        on_delete=models.PROTECT,
        related_name='produtos',
        verbose_name="Categoria"
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )
    
    unidade_medida = models.CharField(
        max_length=20,
        choices=[
            ('UN', 'Unidade'),
            ('KG', 'Quilograma'),
            ('L', 'Litro'),
            ('M', 'Metro'),
            ('M2', 'Metro Quadrado'),
            ('M3', 'Metro Cúbico'),
            ('CX', 'Caixa'),
            ('PCT', 'Pacote'),
        ],
        default='UN',
        verbose_name="Unidade de Medida"
    )
    
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True,
        blank=True,
        verbose_name="Preço Unitário (R$)"
    )
    
    estoque_minimo = models.PositiveIntegerField(
        default=10,
        verbose_name="Estoque Mínimo"
    )
    
    requer_analise = models.BooleanField(
        default=True,
        verbose_name="Requer Análise"
    )
    
    tempo_analise_dias = models.PositiveIntegerField(
        default=7,
        verbose_name="Tempo de Análise (dias)"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['codigo_produto']
    
    def __str__(self):
        return f"{self.codigo_produto} - {self.nome_produto}"
    
    @property
    def estoque_atual(self):
        """Retorna a quantidade total em estoque"""
        return self.estoques.filter(quantidade__gt=0).aggregate(
            total=models.Sum('quantidade')
        )['total'] or 0
    
    @property
    def estoque_disponivel(self):
        """Retorna estoque disponível (aprovado) para uso"""
        return self.estoques.filter(
            quantidade__gt=0,
            status_analise='aprovado'
        ).aggregate(
            total=models.Sum('quantidade')
        )['total'] or 0
    
    @property
    def esta_baixo_estoque(self):
        """Verifica se produto está com estoque baixo"""
        return self.estoque_disponivel <= self.estoque_minimo


class NotaFiscal(models.Model):
    """
    Modelo para notas fiscais
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processada', 'Processada'),
        ('cancelada', 'Cancelada'),
    ]
    
    # ID único da nota fiscal (gerado automaticamente)
    numero_nota = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número da Nota"
    )
    
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name='notas_fiscais',
        verbose_name="Fornecedor"
    )
    
    data_emissao = models.DateField(
        verbose_name="Data de Emissão"
    )
    
    valor_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Total (R$)"
    )
    
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status"
    )
    
    usuario_cadastro = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='notas_fiscais_cadastradas',
        verbose_name="Cadastrado por"
    )
    
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )
    
    data_processamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Processamento"
    )
    
    class Meta:
        verbose_name = "Nota Fiscal"
        verbose_name_plural = "Notas Fiscais"
        ordering = ['-data_emissao', '-data_cadastro']
    
    def __str__(self):
        return f"NF {self.numero_nota} - {self.fornecedor.nome_empresa}"
    
    def save(self, *args, **kwargs):
        # Gerar número único se não fornecido
        if not self.numero_nota:
            # Formato: NF{YYYY}{MM}{sequencial}
            today = datetime.now()
            prefix = f"NF{today.year}{today.month:02d}"
            
            # Buscar último número da sequência
            last_nf = NotaFiscal.objects.filter(
                numero_nota__startswith=prefix
            ).order_by('-numero_nota').first()
            
            if last_nf:
                last_seq = int(last_nf.numero_nota[-4:])
                new_seq = last_seq + 1
            else:
                new_seq = 1
                
            self.numero_nota = f"{prefix}{new_seq:04d}"
        
        super().save(*args, **kwargs)
    
    def processar_entrada_estoque(self):
        """Processa entrada dos itens no estoque"""
        if self.status != 'pendente':
            return False
        
        for item in self.itens_nota.all():
            # Criar entrada no estoque
            Estoque.objects.create(
                produto=item.produto,
                quantidade=item.quantidade,
                lote=item.lote,
                data_fabricacao=item.data_fabricacao,
                data_validade=item.data_validade,
                valor_unitario=item.valor_unitario,
                nota_fiscal=self,
                departamento=Departamento.objects.get(tipo='estoque'),
                status_analise='pendente' if item.produto.requer_analise else 'aprovado'
            )
        
        # Atualizar status da nota
        self.status = 'processada'
        self.data_processamento = datetime.now()
        self.save()
        
        return True


class ItemNotaFiscal(models.Model):
    """
    Modelo para itens de nota fiscal
    """
    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        related_name='itens_nota',
        verbose_name="Nota Fiscal"
    )
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='itens_nota',
        verbose_name="Produto"
    )
    
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantidade"
    )
    
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Unitário (R$)"
    )
    
    lote = models.CharField(
        max_length=50,
        verbose_name="Lote"
    )
    
    data_fabricacao = models.DateField(
        verbose_name="Data de Fabricação"
    )
    
    data_validade = models.DateField(
        verbose_name="Data de Validade"
    )
    
    class Meta:
        verbose_name = "Item de Nota Fiscal"
        verbose_name_plural = "Itens de Nota Fiscal"
        ordering = ['produto__codigo_produto']
    
    def __str__(self):
        return f"{self.produto.codigo_produto} - {self.quantidade} {self.produto.unidade_medida}"
    
    @property
    def valor_total(self):
        """Calcula valor total do item"""
        return self.quantidade * self.valor_unitario


class Estoque(models.Model):
    """
    Modelo para controle de estoque
    """
    STATUS_ANALISE = [
        ('pendente', 'Pendente Análise'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
        ('bloqueado', 'Bloqueado'),
    ]
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='estoques',
        verbose_name="Produto"
    )
    
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Quantidade"
    )
    
    lote = models.CharField(
        max_length=50,
        verbose_name="Lote"
    )
    
    data_fabricacao = models.DateField(
        verbose_name="Data de Fabricação"
    )
    
    data_validade = models.DateField(
        verbose_name="Data de Validade"
    )
    
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Unitário (R$)"
    )
    
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='estoques',
        verbose_name="Departamento Atual"
    )
    
    status_analise = models.CharField(
        max_length=20,
        choices=STATUS_ANALISE,
        default='pendente',
        verbose_name="Status da Análise"
    )
    
    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.PROTECT,
        related_name='estoques',
        verbose_name="Nota Fiscal"
    )
    
    data_entrada = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Entrada"
    )
    
    data_ultima_movimentacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Movimentação"
    )
    
    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f"{self.produto.codigo_produto} - Lote: {self.lote} - Qtd: {self.quantidade}"
    
    @property
    def dias_para_vencimento(self):
        """Retorna quantos dias faltam para o vencimento"""
        from datetime import date
        if self.data_validade:
            delta = self.data_validade - date.today()
            return delta.days
        return None
    
    @property
    def esta_vencido(self):
        """Verifica se o produto está vencido"""
        dias = self.dias_para_vencimento
        return dias is not None and dias < 0
    
    @property
    def esta_proximo_vencimento(self):
        """Verifica se produto está próximo do vencimento (30 dias)"""
        dias = self.dias_para_vencimento
        return dias is not None and 0 <= dias <= 30
    
    @property
    def valor_total_estoque(self):
        """Valor total do estoque (quantidade * valor unitário)"""
        return self.quantidade * self.valor_unitario


class Movimentacao(models.Model):
    """
    Modelo para movimentações de estoque
    """
    TIPOS_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('transferencia', 'Transferência'),
        ('ajuste', 'Ajuste'),
        ('descarte', 'Descarte'),
    ]
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        verbose_name="Produto"
    )
    
    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        verbose_name="Estoque"
    )
    
    tipo_movimentacao = models.CharField(
        max_length=20,
        choices=TIPOS_MOVIMENTACAO,
        verbose_name="Tipo de Movimentação"
    )
    
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantidade"
    )
    
    departamento_origem = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='movimentacoes_origem',
        null=True,
        blank=True,
        verbose_name="Departamento de Origem"
    )
    
    departamento_destino = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='movimentacoes_destino',
        verbose_name="Departamento de Destino"
    )
    
    motivo = models.TextField(
        verbose_name="Motivo/Observações"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        verbose_name="Usuário"
    )
    
    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )
    
    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.tipo_movimentacao} - {self.produto.codigo_produto} - {self.quantidade}"


class AnaliseQualidade(models.Model):
    """
    Modelo para análises de qualidade
    """
    STATUS_ANALISE = [
        ('iniciada', 'Iniciada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    RESULTADO_ANALISE = [
        ('aprovado', 'Aprovado'),
        ('reprovado', 'Reprovado'),
        ('aprovado_condicional', 'Aprovado Condicional'),
    ]
    
    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.PROTECT,
        related_name='analises',
        verbose_name="Estoque"
    )
    
    numero_analise = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número da Análise"
    )
    
    responsavel_analise = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='analises_responsavel',
        verbose_name="Responsável pela Análise"
    )
    
    data_inicio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Início"
    )
    
    data_conclusao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_ANALISE,
        default='iniciada',
        verbose_name="Status"
    )
    
    resultado = models.CharField(
        max_length=30,
        choices=RESULTADO_ANALISE,
        null=True,
        blank=True,
        verbose_name="Resultado"
    )
    
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    
    laudo_tecnico = models.TextField(
        blank=True,
        verbose_name="Laudo Técnico"
    )
    
    class Meta:
        verbose_name = "Análise de Qualidade"
        verbose_name_plural = "Análises de Qualidade"
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"Análise {self.numero_analise} - {self.estoque.produto.codigo_produto}"
    
    def save(self, *args, **kwargs):
        # Gerar número da análise
        if not self.numero_analise:
            today = datetime.now()
            prefix = f"AN{today.year}{today.month:02d}"
            
            last_an = AnaliseQualidade.objects.filter(
                numero_analise__startswith=prefix
            ).order_by('-numero_analise').first()
            
            if last_an:
                last_seq = int(last_an.numero_analise[-4:])
                new_seq = last_seq + 1
            else:
                new_seq = 1
                
            self.numero_analise = f"{prefix}{new_seq:04d}"
        
        super().save(*args, **kwargs)
    
    def finalizar_analise(self, resultado, laudo=''):
        """Finaliza a análise e atualiza o status do estoque"""
        self.resultado = resultado
        self.laudo_tecnico = laudo
        self.status = 'concluida'
        self.data_conclusao = datetime.now()
        self.save()
        
        # Atualizar status do estoque
        status_map = {
            'aprovado': 'aprovado',
            'reprovado': 'reprovado',
            'aprovado_condicional': 'aprovado'
        }
        
        self.estoque.status_analise = status_map[resultado]
        self.estoque.save()
        
        # Se aprovado, mover para departamento industrial
        if resultado in ['aprovado', 'aprovado_condicional']:
            dep_industrial = Departamento.objects.get(tipo='industrial')
            
            Movimentacao.objects.create(
                produto=self.estoque.produto,
                estoque=self.estoque,
                tipo_movimentacao='transferencia',
                quantidade=self.estoque.quantidade,
                departamento_origem=self.estoque.departamento,
                departamento_destino=dep_industrial,
                motivo=f'Produto aprovado na análise {self.numero_analise}',
                usuario=self.responsavel_analise
            )
            
            self.estoque.departamento = dep_industrial
            self.estoque.save()