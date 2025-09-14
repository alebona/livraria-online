from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Livro, Autor, Editora, Categoria
from .forms import BuscarLivroForm
from .functions import *
from core.decorators import perfil_required



@perfil_required('Administrador')
def cadastrar_livro(request):
    if request.method == 'POST':
        form = BuscarLivroForm(request.POST)
        if form.is_valid():
            titulo_input = form.cleaned_data['titulo']

            # Verifica se o livro já existe no banco pelo ISBN (se existir)
            book_info = buscar_livro_google(titulo_input)
            if not book_info:
                messages.error(request, f'Nenhum livro encontrado para "{titulo_input}"')
                return render(request, 'gestao/cadastro_livro.html', {'form': form})
            
            livro_encontrado = verifica_cadastro_livro(book_info)

            if livro_encontrado:
                messages.info(request, f'O livro "{livro_encontrado.titulo}" já está cadastrado.')
                return render(request, 'gestao/cadastro_livro.html', {'form': form, 'livro_existe': True, 'livro': livro_encontrado})

            # Cadastro dos relacionamentos
            autor = verifica_cadastro(Autor, book_info.get('autor', ''), "Autor Desconhecido")
            categoria = verifica_cadastro(Categoria, book_info.get('categoria', ''), "Sem Categoria")
            editora = verifica_cadastro(Editora, book_info.get('editora', ''), "Editora Desconhecida")

            # Tratamento da data de publicação
            data_publicacao = None
            ano_str = book_info.get("data_publicacao")

            if ano_str:
                for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
                    try:
                        data_publicacao = datetime.strptime(ano_str, fmt).date()
                        break
                    except ValueError:
                        continue

            # Criação do livro
            livro = Livro.objects.create(
                titulo=book_info.get('titulo', titulo_input),
                autor=autor,
                editora=editora,
                categoria=categoria,
                data_publicacao=data_publicacao,
                isbn_13=book_info.get('isbn_13', 'N/A'),
                isbn_10=book_info.get('isbn_10', 'N/A'),
                paginas=book_info.get('paginas', 0),
                sinopse=book_info.get('sinopse', 'Sem descrição disponível.'),
                capa=book_info.get('capa', ''),
                rating=book_info.get('rating', 0.0),
                preco = book_info.get('preco', 10.0)
            )

            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('detalhe_livro', pk=livro.pk)

    else:
        form = BuscarLivroForm()

    return render(request, 'gestao/cadastro_livro.html', {'form': form})





