# Livraria Online 📚

Uma aplicação web construída com **Django** que simula uma livraria online, permitindo cadastro de livros, carrinho de compras, finalização de pedidos e histórico de compras. O projeto é modularizado em apps para facilitar manutenção e escalabilidade.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Instalação](#instalação)
- [Uso](#uso)
- [Prints](#prints)

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
├── core/               # Configurações globais, autenticação, páginas base
│    ├── migrations/  
│    └── templates/loja/
│        ├── login.html
│        └── registrar.html  
│    ├── login.html
│    ├── registrar.html   
│    ├── templatetags/  
│    │   └── form_tags.py         
│    ├── admin.py
│    ├── apps.py
│    ├── decorators.py
│    ├── forms.py
│    ├── signals.py
│    ├── tests.py
│    ├── urls.py
│    └── views.py
│  
├── gestao/                # Administração da livraria (cadastros internos)
│    ├── migrations/  
│    ├── templates/gestao/
│        └── cadastro_livro.html
│    ├── admin.py
│    ├── apps.py
│    ├── forms.py
│    ├── functions.py
│    ├── models.py
│    ├── tests.py
│    ├── urls.py
│    └── views.py
│
├── loja/                  # Lado do cliente (carrinho, pedidos, histórico)
│    ├── migrations/
│    └── templates/loja/
│        ├── busca_avancada.html
│        ├── carrinho.html
│        ├── confirmacao_pedido.html
│        ├── detalhe_livro.html
│        ├── detalhe_pedido.html
│        ├── finalizar_pedido.html
│        └── historico_pedidos.html
│    ├── admin.py
│    ├── apps.py
│    ├── context_processors.py
│    ├── models.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py
│
├── livraria_online/       # Configurações do projeto Django
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                # Arquivos estáticos
│   ├── img/
│   │   └── default_book.png
│   └── js/
│       └── loader.js
│   └── estilo.css
│
├── templates/             # Templates globais
│   ├── base.html
│   ├── footer.html
│   └── home.html
│
├── venv/
├── .env
├── .gitignore
├── estrutura_projeto.txt
├── manage.py
├── README.md
└── requirements.txt

````

---

## Modelos de Dados

### `Usuario`
- Extensão do `AbstractUser` com campos adicionais:
  - `perfil` (Cliente, Administrador)
  - `nome_completo`, `endereco`, `numero_endereco`, `bairro`, `cidade`, `estado`, `cep`, `email` .

### `Livro`
- Título, autor, editora, data de publicação, categoria, total de páginas, sinopse, preço, nota, ISBN.

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
python manage.py makemigrations
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

## Prints 



---
