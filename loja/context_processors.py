""" Permitir que o carrinho de compras esteja disponível em todos os templates """
def carrinho_total(request):
    carrinho = request.session.get('carrinho', {})
    total_itens = sum(carrinho.values())
    return {'total_itens_carrinho': total_itens}