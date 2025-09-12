"""
URLs for analytics app
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Relatórios principais
    path('relatorios/', views.relatorios_dashboard, name='relatorios'),
    
    # Relatórios específicos
    path('estoque/', views.relatorio_estoque, name='relatorio_estoque'),
    path('movimentacoes/', views.relatorio_movimentacoes, name='relatorio_movimentacoes'),
    path('vencimentos/', views.relatorio_vencimentos, name='relatorio_vencimentos'),
    path('fornecedores/', views.relatorio_fornecedores, name='relatorio_fornecedores'),
    path('analises/', views.relatorio_analises, name='relatorio_analises'),
    
    # Exportações
    path('export/estoque/', views.export_estoque_excel, name='export_estoque_excel'),
    path('export/movimentacoes/', views.export_movimentacoes_excel, name='export_movimentacoes_excel'),
    path('export/vencimentos/', views.export_vencimentos_excel, name='export_vencimentos_excel'),
    
    # APIs para gráficos
    path('api/estoque-por-departamento/', views.api_estoque_departamento, name='api_estoque_departamento'),
    path('api/movimentacoes-mes/', views.api_movimentacoes_mes, name='api_movimentacoes_mes'),
    path('api/status-analises/', views.api_status_analises, name='api_status_analises'),
    path('api/produtos-vencimento/', views.api_produtos_vencimento, name='api_produtos_vencimento'),
]