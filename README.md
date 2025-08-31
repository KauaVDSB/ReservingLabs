[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Solicita Lab
Plataforma de agendamento e gerenciamento de laboratórios para professores, construída com Flask e SQLAlchemy.

## 📑 Tabela de Conteúdo
- [Funcionalidades](#🚀-funcionalidades)

- [Estrutura do Projeto](#📁-estrutura-do-projeto)

- [Instalação & Configuração](#⚙️-instalação--configuração)

- [Executando a Aplicação](#▶️-executando-a-aplicação)

- [Próximos Passos & Metas](#📅-próximos-passos--metas)

- [Autor](#💻-autor)

## 🚀 Funcionalidades
- CRUD para Laboratórios e Solicitações: Crie, visualize, edite e delete laboratórios e agendamentos.

- Autenticação de Usuários: Sistema de login e cadastro com papéis de "Professor" e "Admin".

- Sistema de Agendamento: Agendamento de laboratórios com validação de horários para evitar conflitos.

- Gerenciamento de Acesso: Permissões de Admin para criar laboratórios, aprovar solicitações e cadastrar novos usuários.

- Cron Job para Status: Um agendador de tarefas em segundo plano atualiza automaticamente o status dos laboratórios para "Disponível" ou "Ocupado".

- Painel de Controle Interativo: Homepage com um calendário dinâmico (FullCalendar.io) para visualizar agendamentos.

- Tabelas Dinâmicas: Listagem de laboratórios com paginação, busca e ordenação.

## 📁 Estrutura do Projeto

```
.
├── app/                      # Pacote principal da aplicação
│   ├── __init__.py           # Inicialização do app, db, migrações e agendador
│   ├── api/                  # Módulo para endpoints da API
│   │   └── agendamentos.py   # Rota de API para o calendário
│   ├── templates/            # Templates Jinja2
│   ├── static/               # Arquivos estáticos (CSS, JS, etc.)
│   ├── models.py             # Definição das classes do banco de dados (SQLAlchemy)
│   ├── forms.py              # Definição dos formulários (Flask-WTF)
│   ├── routes.py             # Rotas principais da aplicação
│   └── scheduler.py          # Lógica do cron job para atualizar status
├── migrations/               # Migrações do Alembic para o banco de dados
├── .env.example              # Exemplo de variáveis de ambiente
├── .flaskenv                 # Configurações para o CLI do Flask
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências do Python
└── wsgi.py                   # Ponto de entrada da aplicação
```

## ⚙️ Instalação & Configuração
**1. Clone o repositório**

```CMD
git clone https://github.com/KauaVDSB/ReservingLabs.git
cd solicita-lab
```
    
**2. Crie e ative um ambiente virtual**

```CMD
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Instale as dependências**

```CMD
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto e adicione as variáveis necessárias.

```
SECRET_KEY='sua-chave-secreta-aqui'
DATABASE_URL='sqlite:///labs.db'
```

**5. Aplique as migrações do banco de dados**
```
flask db upgrade
```

## ▶️ Executando a Aplicação
Inicie o servidor de desenvolvimento:
```
flask run
```
Visite `http://127.0.0.1:5000` para visualizar o projeto.


## 📅 Próximos Passos & Metas
O projeto continuará evoluindo com as seguintes funcionalidades:

- Correção e Implementação do Cron Job: Adicionar a lógica de auto-exclusão para solicitações pendentes e não aprovadas.

- Módulo de Laboratórios: Alterar o campo equipamentos para computadores (tipo integer).

- Módulo de Notificações: Enviar e-mails para os usuários usando Flask-Mail quando suas solicitações forem aceitas, recusadas ou criadas.

- Otimização: Implementar lógica de cache para evitar requisições repetidas ao banco de dados em todas as páginas com dados e aprimorar a lista de laboratórios disponíveis na homepage com paginação.

- Deploy: Preparar a aplicação para deploy em um servidor de produção com banco de dados externo.

## 💻 Autor
**KauaVDSB**

- GitHub: https://github.com/KauaVDSB

- LinkedIn: https://www.linkedin.com/in/kauã-vinicius-dos-santos-barbosa-346b31344

- Email: kauavdsb.jobs@gmail.com
