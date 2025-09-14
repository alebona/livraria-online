from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar-livro/', views.cadastrar_livro, name='cadastrar_livro'),
]
