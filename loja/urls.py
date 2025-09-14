from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("buscar/", views.busca_avancada, name="busca_avancada"),
    path('livro/<int:pk>/', views.detalhe_livro, name='detalhe_livro'),

    #carrinho de compras
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:livro_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:livro_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    #path('carrinho/alterar/<int:livro_id>/<int:quantidade>/', views.alterar_quantidade, name='alterar_quantidade'),

    # finalizando pedido
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('confirmacao/<int:pedido_id>/', views.confirmacao_pedido, name='confirmacao_pedido'),

    # histórico de pedidos
    path("pedidos/", views.historico_pedidos, name="historico_pedidos"),
    path("pedidos/<int:pedido_id>/", views.detalhe_pedido, name="detalhe_pedido"),
    path('historico/exportar/pdf/', views.exportar_historico_pedidos_pdf, name='exportar_historico_pedidos_pdf'),
]
