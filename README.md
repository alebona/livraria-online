# Livraria Online 📚

Uma aplicação web construída com **Django** que simula uma livraria online completa, permitindo cadastro de livros, gerenciamento de estoque, carrinho de compras, finalização de pedidos e histórico de compras. O projeto é modularizado em apps para facilitar manutenção e escalabilidade.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)

---

## Funcionalidades

### Para clientes:
- Cadastro e login de usuários.
- Navegação e busca de livros.
- Carrinho de compras com ajuste de quantidade.
- Seleção de forma de pagamento (`Pix`, `Boleto` ou `Cartão de Crédito`).
- Finalização de pedidos com status definido automaticamente:
  - **Pix** → Aprovado
  - **Boleto / Cartão de Crédito** → Pendente
- Histórico de pedidos com exportação em PDF.
- Visualização detalhada de cada pedido.

### Para administradores:
- Cadastro e gestão de livros.
- Cadastro de autores, categorias e editoras.
- Gestão de pedidos (visualização e atualização de status).

---

## Tecnologias

- **Backend:** Python 3.13, Django 5.2
- **Frontend:** HTML5, Bootstrap 5, Bootstrap Icons
- **Banco de Dados:** PostgreSQL
- **PDF Export:** ReportLab
- **Controle de versões:** Git

---

## Estrutura do Projeto

```

livraria-online/
│
├── core/                  # Configurações globais, autenticação, páginas base
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
│
├── gestao/                # Administração da livraria
│   ├── models.py          # Livro, Autor, Categoria, Editora...
│   ├── views.py
│   ├── urls.py
│   └── templates/gestao/
│
├── loja/                  # Lado do cliente (carrinho, pedidos, checkout)
│   ├── models.py          # Pedido, ItemPedido, Carrinho
│   ├── views.py
│   ├── urls.py
│   └── templates/loja/
│
├── static/                # Arquivos estáticos (CSS, JS, imagens)
├── templates/             # Templates globais (base.html, footer.html, home.html)
├── manage.py
└── requirements.txt

````

---

## Modelos de Dados

### `Usuario`
- Extensão do `AbstractUser` com campos adicionais:
  - `perfil` (Cliente, Administrador)
  - `nome_completo`, `telefone`, `endereco` etc.

### `Livro`
- Título, autor, editora, categoria, preço, estoque, ISBN.

### `Pedido`
- Usuário associado.
- Data de criação.
- Forma de pagamento.
- Status (`A` = Aprovado, `P` = Pendente, `C` = Cancelado).
- Total.

### `ItemPedido`
- Pedido associado.
- Livro associado.
- Quantidade.
- Subtotal.

---

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/livraria-online.git
cd livraria-online
````

2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

4. Configure o `.env` com variáveis sensíveis (ex: SECRET\_KEY, DB).

5. Rode as migrações:

```bash
python manage.py migrate
```

6. Crie um superusuário para administração:

```bash
python manage.py createsuperuser
```

7. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

---

## Uso

* Acesse `http://127.0.0.1:8000/` para usar a loja.
* Clientes podem navegar, adicionar ao carrinho e finalizar pedidos.
* Administradores podem acessar a área de gestão para cadastrar livros.

---

## Contribuição

Pull requests são bem-vindos!
Antes de enviar, siga estas recomendações:

1. Atualize o repositório local.
2. Crie uma branch para a feature:

```bash
git checkout -b feature/nova-funcionalidade
```

3. Faça commit das mudanças:

```bash
git commit -m "Descrição da mudança"
```

4. Envie para o repositório remoto:

```bash
git push origin feature/nova-funcionalidade
```

5. Abra um Pull Request.

---
