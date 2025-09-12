"""
Views for analytics and reporting
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def relatorios_dashboard(request):
    """Dashboard de relatórios"""
    return render(request, 'analytics/relatorios_dashboard.html')


@login_required
def relatorio_estoque(request):
    """Relatório de estoque"""
    return render(request, 'analytics/relatorio_estoque.html')


@login_required
def relatorio_movimentacoes(request):
    """Relatório de movimentações"""
    return render(request, 'analytics/relatorio_movimentacoes.html')


@login_required
def relatorio_vencimentos(request):
    """Relatório de vencimentos"""
    return render(request, 'analytics/relatorio_vencimentos.html')


@login_required
def relatorio_fornecedores(request):
    """Relatório de fornecedores"""
    return render(request, 'analytics/relatorio_fornecedores.html')


@login_required
def relatorio_analises(request):
    """Relatório de análises"""
    return render(request, 'analytics/relatorio_analises.html')


@login_required
def export_estoque_excel(request):
    """Exportar estoque em Excel"""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=estoque.xlsx'
    return response


@login_required
def export_movimentacoes_excel(request):
    """Exportar movimentações em Excel"""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=movimentacoes.xlsx'
    return response


@login_required
def export_vencimentos_excel(request):
    """Exportar vencimentos em Excel"""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=vencimentos.xlsx'
    return response


@login_required
def api_estoque_departamento(request):
    """API para gráfico de estoque por departamento"""
    return JsonResponse({'success': True})


@login_required
def api_movimentacoes_mes(request):
    """API para gráfico de movimentações por mês"""
    return JsonResponse({'success': True})


@login_required
def api_status_analises(request):
    """API para gráfico de status de análises"""
    return JsonResponse({'success': True})


@login_required
def api_produtos_vencimento(request):
    """API para gráfico de produtos próximos ao vencimento"""
    return JsonResponse({'success': True})