from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Livro, Autor, Editora, Categoria
from .forms import BuscarLivroForm
from .functions import *
from core.decorators import perfil_required



@perfil_required('Administrador')
def pesquisar_livro(request):
    if request.method == 'POST':
        form = BuscarLivroForm(request.POST)
        if form.is_valid():
            titulo_input = form.cleaned_data['titulo']
            autor_input = form.cleaned_data.get('autor')  # se tiver no form

            resultados = buscar_livro_google(titulo_input, autor_input)

            if not resultados:
                messages.error(request, f'Nenhum livro encontrado para "{titulo_input}"')
                return render(request, 'gestao/cadastro_livro.html', {'form': form})

            # Mostra lista para o usuário escolher
            return render(request, 'gestao/cadastro_livro.html', {
                'form': form,
                'resultados': resultados
            })

    else:
        form = BuscarLivroForm()

    return render(request, 'gestao/cadastro_livro.html', {'form': form})



@perfil_required('Administrador')
def importar_livro(request):
    if request.method != "POST":
        messages.error(request, "Método inválido.")
        return redirect('pesquisar_livro')

    ids_selecionados = request.POST.getlist('ids_google[]')
    if not ids_selecionados:
        messages.warning(request, "Nenhum livro selecionado para importação.")
        return redirect('pesquisar_livro')

    importados = []
    ja_cadastrados = []

    for id_google in ids_selecionados:
        # Recupera os dados do hidden inputs
        book_info = {
            "titulo": request.POST.get(f'titulos_{id_google}', ''),
            "autor": request.POST.get(f'autores_{id_google}', 'Autor Desconhecido'),
            "editora": request.POST.get(f'editoras_{id_google}', 'Editora Desconhecida'),
            "categoria": request.POST.get(f'categorias_{id_google}', 'Sem Categoria'),
            "data_publicacao": request.POST.get(f'datas_publicacao_{id_google}', None),
            "sinopse": request.POST.get(f'sinopses_{id_google}', 'Sem descrição disponível.'),
            "capa": request.POST.get(f'capas_{id_google}', ''),
            "isbn_13": request.POST.get(f'isbn_13s_{id_google}', 'N/A'),
            "isbn_10": request.POST.get(f'isbn_10s_{id_google}', 'N/A'),
            "paginas": request.POST.get(f'paginas_{id_google}', 0),
            "rating": request.POST.get(f'ratings_{id_google}', 0.0),
            "preco": request.POST.get(f'precos_{id_google}', 10.0)
        }

        # Corrige vírgula para ponto
        book_info['preco'] = str(book_info['preco']).replace(',', '.')
        book_info['rating'] = str(book_info['rating']).replace(',', '.')

        # Verifica duplicidade
        if verifica_cadastro_livro(book_info):
            ja_cadastrados.append(book_info['titulo'])
            continue

        # Relacionamentos
        autor_obj = verifica_cadastro(Autor, book_info['autor'], "Autor Desconhecido")
        categoria_obj = verifica_cadastro(Categoria, book_info['categoria'], "Sem Categoria")
        editora_obj = verifica_cadastro(Editora, book_info['editora'], "Editora Desconhecida")

        # Data de publicação
        data_publicacao = None
        ano_str = book_info['data_publicacao']
        if ano_str:
            for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
                try:
                    data_publicacao = datetime.strptime(ano_str, fmt).date()
                    break
                except ValueError:
                    continue

        # Criação
        livro = Livro.objects.create(
            titulo=book_info['titulo'],
            autor=autor_obj,
            editora=editora_obj,
            categoria=categoria_obj,
            data_publicacao=data_publicacao,
            isbn_13=book_info['isbn_13'],
            isbn_10=book_info['isbn_10'],
            paginas=int(book_info['paginas']) if book_info['paginas'] else 0,
            sinopse=book_info['sinopse'],
            capa=book_info['capa'],
            rating=float(book_info['rating']) if book_info['rating'] else 0.0,
            preco=float(book_info['preco']) if book_info['preco'] else 10.0
        )

        importados.append(livro.titulo)

    if importados:
        messages.success(request, f'Livros importados com sucesso: {", ".join(importados)}')
    if ja_cadastrados:
        messages.info(request, f'Já cadastrados: {", ".join(ja_cadastrados)}')

    return redirect('pesquisar_livro')







