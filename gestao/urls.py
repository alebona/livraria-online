from django.urls import path
from . import views

urlpatterns = [
    path('pesquisar-livro/', views.pesquisar_livro, name='pesquisar_livro'),
    path('importar-livro/', views.importar_livro, name='importar_livro'),
]
