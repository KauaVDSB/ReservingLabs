# Import das bibliotecas necessárias na inicialização
#precisa reconhecer as variaveis, classes e bibliotecas para poder começar a fazer alterações

import os  #mexer no sistema operacional (ler arquivos)

from flask import Flask  #função principal
from flask_sqlalchemy import SQLAlchemy  #CRUD
from flask_migrate import Migrate  #modelo-->bd
from flask_bcrypt import Bcrypt  #criptografia//segurança
from flask_login import LoginManager  #autodescritivo
from apscheduler.schedulers.background import BackgroundScheduler  #agendador de tarefas
import atexit  #encerrar tarefas

from dotenv import load_dotenv

load_dotenv(".env")  # Carrega dados do arquivo .env


# Inicializa e configura a aplicação
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  #verifica o arquivo .env, se houver a chave, o servidor funciona normalmente
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa ferramentas para manipulação do banco de dados
db = SQLAlchemy(app)  #não é pasta, e sim a variavel app
migrate = Migrate(app, db)  #inicializa variavel
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = (
    "login"  # Redireciona usuários para esta rota, caso estejam deslogados.
)

from app.models import User, Laboratorio, Solicitacao

# Importa rotas necessárias na inicialização do app
from app.routes import homepage, login
from app.api.agendamentos import api_agendamentos

# Configurações do Cron Job
from app.scheduler import atualizar_status_laboratorios

scheduler = BackgroundScheduler()
# Agenda tarefa para rodar a cada 5 minutos
scheduler.add_job(
    func=atualizar_status_laboratorios,
    trigger="interval",
    minutes=5
)
scheduler.start()

# Desliga agendador ao fechar app
atexit.register(lambda: scheduler.shutdown())
