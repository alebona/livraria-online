# Livraria Online 📚

Uma aplicação web construída com **Django** que simula uma livraria online, permitindo cadastro de livros, carrinho de compras, finalização de pedidos e histórico de compras. O projeto é modularizado em apps para facilitar manutenção e escalabilidade.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Carrinho de Compras](#carrinho-de-compras)
- [Perfil do Usuário](#perfil-do-usuário)
- [Pesquisa de Livros](#pesquisa-de-livros)
- [Instalação](#instalação)
- [Uso](#uso)
- [Diagrama de Modelos](#diagrama-de-modelos)
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
- Cadastro de livros.
- Cadastro de autores, categorias e editoras.

---

## Tecnologias

- **Backend:** Python 3.13, Django 5.2
- **Frontend:** HTML5, Bootstrap 5, Bootstrap Icons
- **Banco de Dados:** PostgreSQL
- **Bibliotecas/Pacotes:**
  - **asgiref 3.9.1** – Suporte ASGI para Django
  - **certifi 2025.8.3** – Certificados SSL confiáveis
  - **charset-normalizer 3.4.3** – Normalização de encoding
  - **django-environ 0.12.0** – Gerenciamento de variáveis de ambiente
  - **pillow 11.3.0** – Manipulação de imagens
  - **psycopg2-binary 2.9.10** – Conector PostgreSQL
  - **reportlab 4.4.3** – Geração de PDFs
  - **requests 2.32.5** – Requisições HTTP para APIs externas
  - **sqlparse 0.5.3** – Parsing de SQL
  - **tzdata 2025.2** – Fuso horário
  - **urllib3 2.5.0** – Cliente HTTP
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
│        ├── perfil\_usuario.html
│        └── registrar.html
│    ├── templatetags/
│    │   └── form\_tags.py
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
│        └── cadastro\_livro.html
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
│        ├── busca\_avancada.html
│        ├── carrinho.html
│        ├── confirmacao\_pedido.html
│        ├── detalhe\_livro.html
│        ├── detalhe\_pedido.html
│        ├── finalizar\_pedido.html
│        └── historico\_pedidos.html
│    ├── admin.py
│    ├── apps.py
│    ├── context\_processors.py
│    ├── models.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py
│
├── livraria\_online/       # Configurações do projeto Django
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                # Arquivos estáticos
│   ├── img/
│   │   └── default\_book.png
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
├── estrutura\_projeto.txt
├── manage.py
├── README.md
└── requirements.txt

````

---

## Modelos de Dados

### `Usuario`
- Extensão do `AbstractUser` com campos adicionais:
  - `perfil` (Cliente, Administrador)
  - `nome_completo`, `endereco`, `numero_endereco`, `bairro`, `cidade`, `estado`, `cep`, `email`.

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

### `Carrinho`
- Usuário associado.
- Itens armazenados em `ItemCarrinho`.

### `ItemCarrinho`
- Carrinho associado.
- Livro associado.
- Quantidade.

---

## Carrinho de Compras

- Permite adicionar livros, alterar quantidades e remover itens.
- Persistência de carrinho:
  - **Usuário logado:** salvo no banco e carregado automaticamente em futuras sessões.
  - **Usuário não logado:** mantido na sessão do navegador.
- Subtotal e total do pedido calculados dinamicamente.
- Ao finalizar o pedido:
  - Grava em `Pedido` e `ItemPedido`.
  - Limpa o carrinho na sessão e no banco.

---

## Perfil do Usuário

- Página de perfil com informações pessoais.
- Formulário **pré-preenchido** e editável.
- Campos:
  - Nome completo, endereço, número, bairro, cidade, estado, CEP e email.
- Mensagem de sucesso exibida após salvar:  
  `Perfil atualizado com sucesso!`

---

## Pesquisa de Livros

- Pesquisa por **título**, **autor** ou ambos.
- Importação da **API Google Books** para banco interno.
- Evita duplicidade usando `ISBN-13` e `ISBN-10`.
- Campos importados:
  - Título, autor, editora, categoria, data de publicação, número de páginas, sinopse, preço, nota, ISBN.

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

6. Crie um superusuário:

```bash
python manage.py createsuperuser
```

7. Inicie o servidor:

```bash
python manage.py runserver
```

---

## Uso

* Acesse `http://127.0.0.1:8000/` para usar a loja.
* Clientes podem navegar, adicionar ao carrinho e finalizar pedidos.
* Administradores acessam a área de gestão para cadastrar livros e gerenciar pedidos.

---

## Diagrama de Modelos

```text
Usuario
 ├─> perfil (Cliente / Administrador)
 ├─> nome_completo
 └─> endereco, numero, bairro, cidade, estado, cep, email

Livro
 ├─> titulo, autor, editora, categoria
 ├─> data_publicacao, paginas, sinopse
 └─> preco, rating, isbn_13, isbn_10

Pedido
 ├─> user
 ├─> total
 ├─> forma_pagamento
 ├─> status
 └─> Itens -> ItemPedido

ItemPedido
 ├─> pedido
 ├─> livro
 ├─> quantidade
 └─> subtotal

Carrinho
 ├─> user
 └─> Itens -> ItemCarrinho

ItemCarrinho
 ├─> carrinho
 ├─> livro
 └─> quantidade
```

---

## Prints

### Cadastro
<img width="1917" height="905" alt="cadastro" src="https://github.com/user-attachments/assets/bb5ee23e-34dd-4c30-ba82-c4a89a788072" />

### Login
<img width="1917" height="907" alt="login" src="https://github.com/user-attachments/assets/bb6f71af-212e-49ff-aa72-eac5289ebedf" />

### Home
<img width="1912" height="907" alt="home" src="https://github.com/user-attachments/assets/91c719a1-c30f-4f78-8a25-578aedd4d0e4" />

### Pesquisa de Livros
<img width="1919" height="933" alt="busca_avancada" src="https://github.com/user-attachments/assets/73447fab-1f48-4688-a750-61a1bbc018f2" />

### Carrinho
<img width="1915" height="910" alt="carrinho" src="https://github.com/user-attachments/assets/54854a16-db67-453d-a440-0aa2a1dc081d" />

### Pedidos
<img width="1915" height="905" alt="pedidos" src="https://github.com/user-attachments/assets/74ec13f4-7014-4f55-8ec6-5c9651986dca" />

### Consulta na API Google Books
<img width="1911" height="908" alt="pesquisa_cadastro" src="https://github.com/user-attachments/assets/67b321e1-e66a-4d03-97f2-17cbc12748db" />

### Importar Livros 
<img width="1910" height="917" alt="importar" src="https://github.com/user-attachments/assets/70c01a7e-3a48-4cd6-bf19-3aedeb1ddf3c" />

### Perfil de Usuário
<img width="1913" height="890" alt="perfil" src="https://github.com/user-attachments/assets/34d1ade3-7588-4a11-80f9-23090ec80e46" />






