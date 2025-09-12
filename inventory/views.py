"""
Views for inventory management
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
def entrada_list(request):
    """Lista de entradas de produtos"""
    return render(request, 'inventory/entrada_list.html')


@login_required
def processar_entrada(request, nota_id):
    """Processar entrada de produtos"""
    return JsonResponse({'success': True})


@login_required
def movimentacao_list(request):
    """Lista de movimentações"""
    return render(request, 'inventory/movimentacao_list.html')


@login_required
def nova_movimentacao(request):
    """Nova movimentação"""
    return render(request, 'inventory/nova_movimentacao.html')


@login_required
def movimentacao_detail(request, movimentacao_id):
    """Detalhes da movimentação"""
    return render(request, 'inventory/movimentacao_detail.html')


@login_required
def analise_list(request):
    """Lista de análises"""
    return render(request, 'inventory/analise_list.html')


@login_required
def nova_analise(request, estoque_id):
    """Nova análise"""
    return render(request, 'inventory/nova_analise.html')


@login_required
def analise_detail(request, analise_id):
    """Detalhes da análise"""
    return render(request, 'inventory/analise_detail.html')


@login_required
def finalizar_analise(request, analise_id):
    """Finalizar análise"""
    return JsonResponse({'success': True})


@login_required
def fornecedor_list(request):
    """Lista de fornecedores"""
    return render(request, 'inventory/fornecedor_list.html')


@login_required
def fornecedor_create(request):
    """Criar fornecedor"""
    return render(request, 'inventory/fornecedor_create.html')


@login_required
def fornecedor_detail(request, fornecedor_id):
    """Detalhes do fornecedor"""
    return render(request, 'inventory/fornecedor_detail.html')


@login_required
def fornecedor_edit(request, fornecedor_id):
    """Editar fornecedor"""
    return render(request, 'inventory/fornecedor_edit.html')


@login_required
def produto_list(request):
    """Lista de produtos"""
    return render(request, 'inventory/produto_list.html')


@login_required
def produto_create(request):
    """Criar produto"""
    return render(request, 'inventory/produto_create.html')


@login_required
def produto_detail(request, produto_id):
    """Detalhes do produto"""
    return render(request, 'inventory/produto_detail.html')


@login_required
def produto_edit(request, produto_id):
    """Editar produto"""
    return render(request, 'inventory/produto_edit.html')


@login_required
def estoque_list(request):
    """Lista de estoque"""
    return render(request, 'inventory/estoque_list.html')


@login_required
def estoque_detail(request, estoque_id):
    """Detalhes do estoque"""
    return render(request, 'inventory/estoque_detail.html')


@require_http_methods(["GET"])
def ajax_produto_info(request, produto_id):
    """Informações do produto via AJAX"""
    return JsonResponse({'success': True})


@require_http_methods(["GET"])
def ajax_estoque_disponivel(request, produto_id):
    """Estoque disponível do produto via AJAX"""
    return JsonResponse({'success': True})