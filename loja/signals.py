from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from loja.models import Carrinho, ItemCarrinho

@receiver(user_logged_in)
def carregar_carrinho(sender, user, request, **kwargs):
    """
    Carrega itens do carrinho do banco para a sessão após login,
    mas mantém os itens da sessão (caso o usuário já tenha removido algo).
    """
    session_carrinho = request.session.get("carrinho", {})

    carrinho_obj, _ = Carrinho.objects.get_or_create(user=user)
    itens_banco = ItemCarrinho.objects.filter(carrinho=carrinho_obj)

    for item in itens_banco:
        # Se o livro já existe na sessão, mantém a quantidade da sessão
        if str(item.livro.id) not in session_carrinho:
            session_carrinho[str(item.livro.id)] = item.quantidade

    request.session["carrinho"] = session_carrinho
    request.session.modified = True

