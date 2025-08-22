# Import das bibliotecas necessárias na inicialização

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from dotenv import load_dotenv

load_dotenv(".env")  # Carrega dados do arquivo .env


# Inicializa e configura a aplicação
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa ferramentas para manipulação do banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = (
    "login"  # Redireciona usuários para esta rota, caso estejam deslogados.
)

from app.models import User, Laboratorio, Solicitacao

# Importa rotas necessárias na inicialização do app
from app.routes import homepage, login
