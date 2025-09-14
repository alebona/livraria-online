from urllib.parse import quote_plus
import requests
from django.db.models import Q
from gestao.models import Livro
from pprint import pprint


def verifica_cadastro(model, nome, default="Desconhecido"):
    """
    Função para verificar se autor, editora ou categoria já está cadastrado
    """
    if not nome:
        nome = default
    obj, _ = model.objects.get_or_create(nome=nome)
    return obj

from urllib.parse import quote_plus
import requests
from pprint import pprint

def buscar_livro_google(titulo):
    """
    Busca um livro no Google Books pelo título e retorna os dados principais.
    """
    query = quote_plus(titulo)
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1"
    response = requests.get(url)
    data = response.json()

    if "items" not in data or len(data["items"]) == 0:
        return None

    # Seleciona o item com maior rating
    items = data["items"]
    items.sort(key=lambda x: x.get("volumeInfo", {}).get("averageRating", 0), reverse=True)
    book_info = items[0]["volumeInfo"]

    # ISBNs
    isbn_13 = "N/A"
    isbn_10 = "N/A"
    for identifier in book_info.get("industryIdentifiers", []):
        if identifier["type"] == "ISBN_13":
            isbn_13 = identifier["identifier"]
        elif identifier["type"] == "ISBN_10":
            isbn_10 = identifier["identifier"]

    # Preço
    sale_info = items[0].get("saleInfo", {})
    preco = None
    if sale_info.get("saleability") == "FOR_SALE":
        list_price = sale_info.get("listPrice")
        if list_price:
            preco = list_price.get("amount")

    dados = {
        "titulo": book_info.get("title", titulo),
        "autor": ", ".join(book_info.get("authors", [])) or "Autor Desconhecido",
        "editora": book_info.get("publisher", "Editora Desconhecida"),
        "data_publicacao": book_info.get("publishedDate", "1901-01-01"),
        "sinopse": book_info.get("description", ""),
        "isbn_13": isbn_13,
        "isbn_10": isbn_10,
        "paginas": book_info.get("pageCount", 0),
        "categoria": ", ".join(book_info.get("categories", [])) or "Sem Categoria",
        "rating": book_info.get("averageRating", 0),
        "capa": book_info.get("imageLinks", {}).get("thumbnail", ""),
        "preco": preco if preco is not None else 10.0
    }

    return dados


def verifica_cadastro_livro(book_info):
    
    isbn_13 = book_info.get('isbn_13')
    isbn_10 = book_info.get('isbn_10')
    livro_encontrado = None

    # aplica a lógica de verificação apenas se pelo menos um dos ISBNs for válido
    if isbn_13 != "N/A" or isbn_10 != "N/A":
        q = Q()
        if isbn_13 != "N/A":
            q |= Q(isbn_13=isbn_13)
        if isbn_10 != "N/A":
            q |= Q(isbn_10=isbn_10)

        # Verifica se o livro já existe pelo ISBN 13 ou ISBN 10
        livro_encontrado = Livro.objects.filter(q).first()

    if livro_encontrado:
        return True

    return False


