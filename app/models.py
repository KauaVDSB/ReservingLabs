from flask_login import UserMixin #reconhecer tabela de usuarios

from app import db, login_manager #pasta app/__init__.py
import datetime #salvar horarios


@login_manager.user_loader #identificador da função
def load_user(user_id):
    """ Função wrapper para recuperar dados do usuário. """
      #mantem os usuarios logados
    return User.query.get(int(user_id)) #verificar dados do usuario do tal id


class User(db.Model, UserMixin):
    """
    Classe para usuários, sendo eles professores,
    admins ou ambos simultaneamente.

    * 'db.Model' mapeia a classe para a tabela
    * 'UserMixin' fornece implementações padrão para a integração com o Flask-Login.
    """

    # nome da tabela no banco de dados
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  #unicidade de e-mail
    # a senha é criptografada antes de salva
    senha = db.Column(db.String(200), nullable=False)

    # flags que definem se o usuário é professor ou admin (0=False, 1=True)
    #por padrão o usuario começa como professor apenas, afinal o publico alvo são eles
    professor = db.Column(db.Integer, default=1, nullable=False)
    admin = db.Column(db.Integer, default=0, nullable=False)

    """
    'db.relationship' define a relação entre esta classe e a classe 'Solicitacao'.
    * A relação é um-para-muitos: um User pode ter muitas Solicitacoes.
    * 'Solicitacao' é o nome da classe relacionada.
    * 'back_populates' cria a ligação bidirecional, ligando a este objeto
    a propriedade 'user' na classe Solicitacao.
    """
    solicitacoes = db.relationship(
        'Solicitacao', back_populates='user', lazy=True  #relacionando uma tabela com outra
    )



class Laboratorio(db.Model):
    """ Representa a tabela de laboratorios """
    __tablename__ = 'labs'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    equipamentos = db.Column(db.String(200), nullable=False)
    abertura = db.Column(db.Time, nullable=False)
    fechamento = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(12), default="Disponível", nullable=False)

    """ Relacao um-para-muitos: Um laboratorio pode ter muitas Solicitacoes. 
        aponta para lab em Solicitacao.
    """
    solicitacoes = db.relationship(
        'Solicitacao', back_populates='lab', lazy=True
    )



class Solicitacao(db.Model):
    """ Representa as solicitacoes de laboratorios. """

    __tablename__ = 'solicitacoes'

    id = db.Column(db.Integer, primary_key=True)

    data_solicitacao = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    # Datas de inicio e fim da reserva.
    data_agendada = db.Column(db.DateTime, nullable=False)
    data_encerramento = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(20), default="Pendente", nullable=False)

    # 'db.ForeignKey' define a chave estrangeira.
    # Estas colunas referenciam os 'id' das tabela referentes.
    # É o lado "muitos" da relação.
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_lab = db.Column(db.Integer, db.ForeignKey('labs.id'), nullable=False)


    # Relações bidirecionais que ligam de volta às classes User e Laboratorio.
    # Permite acessar os objetos User e Laboratorio a partir de um objeto Solicitacao.
    # 'back_populates' aponta para a propriedade 'solicitacoes' na classe User e Laboratorio.
    user = db.relationship('User', back_populates='solicitacoes')
    lab = db.relationship('Laboratorio', back_populates='solicitacoes')


