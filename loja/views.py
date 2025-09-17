from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from gestao.models import Autor, Categoria, Livro
from time import time
from core.decorators import login_required
from django.contrib import messages
from loja.models import Carrinho, ItemCarrinho, ItemPedido, Pedido
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from django.db import transaction

def home(request):
    # Busca os top 12 livros (pode ser por rating, por exemplo) e excluindo sem categoria
    categoria_id = Categoria.objects.values_list('id', flat=True).get(nome='Sem Categoria')

    top_livros = Livro.objects.all().exclude(categoria=categoria_id).order_by('-rating')[:12]

    return render(request, 'home.html', {
        'top_livros': top_livros,
        'timestamp': int(time()),
    })


def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'loja/detalhe_livro.html', {'livro': livro})


def busca_avancada(request):
    titulo = request.GET.get('titulo', '')
    autor_id = request.GET.get('autor')
    categoria_id = request.GET.get('categoria')

    livros = Livro.objects.all()

    if titulo:
        livros = livros.filter(titulo__icontains=titulo)
    if autor_id:
        livros = livros.filter(autor_id=autor_id)
    if categoria_id:
        livros = livros.filter(categoria_id=categoria_id)

    autores = Autor.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'loja/busca_avancada.html', {
        'livros': livros,
        'autores': autores,
        'categorias': categorias
    })



""" Carrinho de Compras """

def adicionar_carrinho(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)

    if request.user.is_authenticated:
        carrinho, _ = Carrinho.objects.get_or_create(user=request.user)

        # Pega item existente ou cria
        item, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, livro=livro)

        if not created:
            item.quantidade += 1
        else:
            item.quantidade = 1

        item.save()

        # Atualiza sessão com todos os itens do carrinho
        request.session['carrinho'] = {
            str(i.livro.id): i.quantidade for i in ItemCarrinho.objects.filter(carrinho=carrinho)
        }
        request.session.modified = True

    else:
        # Sessão para usuário não logado
        carrinho_sessao = request.session.get('carrinho', {})
        carrinho_sessao[str(livro.id)] = carrinho_sessao.get(str(livro.id), 0) + 1
        request.session['carrinho'] = carrinho_sessao
        request.session.modified = True

    return redirect('ver_carrinho')




def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    livros = []
    total = 0

    for livro_id, quantidade in carrinho.items():
        livro = get_object_or_404(Livro, pk=livro_id)
        subtotal = livro.preco * quantidade
        livros.append({
            'livro': livro,
            'quantidade': quantidade,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'loja/carrinho.html', {'livros': livros, 'total': total})


def remover_do_carrinho(request, livro_id):
    livro_id_str = str(livro_id)

    # Remove da sessão
    carrinho = request.session.get('carrinho', {})
    if livro_id_str in carrinho:
        del carrinho[livro_id_str]
        request.session['carrinho'] = carrinho
        request.session.modified = True

    # Remove do banco se usuário estiver logado
    if request.user.is_authenticated:
        carrinho_obj = Carrinho.objects.filter(user=request.user).first()
        if carrinho_obj:
            ItemCarrinho.objects.filter(carrinho=carrinho_obj, livro_id=livro_id).delete()

    return redirect('ver_carrinho')


def alterar_quantidade(request, livro_id, quantidade):
    carrinho = request.session.get('carrinho', {})
    livro_id_str = str(livro_id)

    if livro_id_str in carrinho:
        if quantidade > 0:
            carrinho[livro_id_str] = quantidade
        else:
            del carrinho[livro_id_str]

        request.session['carrinho'] = carrinho
        request.session.modified = True

        # Atualiza banco se usuário logado
        if request.user.is_authenticated:
            carrinho_obj = Carrinho.objects.filter(user=request.user).first()
            if carrinho_obj:
                item = ItemCarrinho.objects.filter(carrinho=carrinho_obj, livro_id=livro_id).first()
                if item:
                    if quantidade > 0:
                        item.quantidade = quantidade
                        item.save()
                    else:
                        item.delete()

    return redirect('ver_carrinho')


""" Finalizando o pedido """
@login_required
def finalizar_pedido(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.info(request, "O carrinho está vazio.")
        return redirect('home')

    livros = []
    total = 0
    for livro_id, quantidade in carrinho.items():
        livro = get_object_or_404(Livro, pk=livro_id)
        subtotal = livro.preco * quantidade
        livros.append({'livro': livro, 'quantidade': quantidade, 'subtotal': subtotal})
        total += subtotal

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        if not forma_pagamento:
            messages.error(request, "Escolha uma forma de pagamento.")
            return redirect('finalizar_pedido')

        status = "A" if forma_pagamento.lower() == "pix" else "P"

        try:
            with transaction.atomic():
                pedido = Pedido.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    total=total,
                    forma_pagamento=forma_pagamento,
                    status=status
                )

                for item in livros:
                    ItemPedido.objects.create(
                        pedido=pedido,
                        livro=item['livro'],
                        quantidade=item['quantidade'],
                        subtotal=item['subtotal']
                    )

                # Limpa o carrinho da sessão
                request.session['carrinho'] = {}
                request.session.modified = True

                if request.user.is_authenticated:
                    carrinho_obj = Carrinho.objects.filter(user=request.user).first()
                    if carrinho_obj:
                        ItemCarrinho.objects.filter(carrinho=carrinho_obj).delete()
                        carrinho_obj.delete()

            messages.success(request, f"Pedido #{pedido.id} finalizado com sucesso!")
            return redirect('confirmacao_pedido', pedido_id=pedido.id)

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao finalizar o pedido: {str(e)}")
            return redirect('finalizar_pedido')

    return render(request, 'loja/finalizar_pedido.html', {'livros': livros, 'total': total})


@login_required
def confirmacao_pedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    return render(request, 'loja/confirmacao_pedido.html', {'pedido': pedido})

""" Visualizando os pedidos do usuário """
@login_required
def historico_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by("-data_criacao")
    return render(request, "loja/historico_pedidos.html", {"pedidos": pedidos})

@login_required
def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, user=request.user)
    itens = []

    for item in pedido.itens.all():
        itens.append({
            "livro": item.livro,
            "quantidade": item.quantidade,
            "subtotal": item.subtotal,
            "preco_unitario": item.subtotal / item.quantidade if item.quantidade else 0,
        })

    return render(request, "loja/detalhe_pedido.html", {"pedido": pedido, "itens": itens})

@login_required
def exportar_historico_pedidos_pdf(request):
    # Garante que só usuários logados vejam seus pedidos
    if not request.user.is_authenticated:
        return redirect('login')

    # Recupera pedidos do usuário
    pedidos = Pedido.objects.filter(user=request.user).order_by('-data_criacao')

    # Configura a resposta HTTP como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historico_pedidos.pdf"'

    # Cria o PDF
    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Data de impressão 
    data_impressao = datetime.now().strftime("%d/%m/%Y %H:%M")
    p.setFont("Helvetica", 8)
    p.drawRightString(largura - 40, altura - 30, f"Impresso em: {data_impressao}")

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, altura - 50, f"Histórico de Pedidos - Livraria Online")



    # Nome do cliente
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, altura - 80, f"Cliente: {request.user.nome_completo}")

    # Cabeçalho
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, altura - 110, "ID")
    p.drawString(120, altura - 110, "Data")
    p.drawString(250, altura - 110, "Pagamento")
    p.drawString(350, altura - 110, "Status")
    p.drawString(450, altura - 110, "Total")

    # Conteúdo
    y = altura - 120
    p.setFont("Helvetica", 11)

    for pedido in pedidos:
        p.drawString(50, y, str(pedido.id))
        p.drawString(120, y, pedido.data_criacao.strftime("%d/%m/%Y %H:%M"))
        p.drawString(250, y, pedido.forma_pagamento)
        p.drawString(350, y, pedido.get_status_display_text())
        p.drawString(450, y, f"R$ {pedido.total:.2f}")
        y -= 20

        # Quebra de página se necessário
        if y < 50:
            p.showPage()
            y = altura - 50
            p.setFont("Helvetica", 11)

    p.showPage()
    p.save()
    return response




