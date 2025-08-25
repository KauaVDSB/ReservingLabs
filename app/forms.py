from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    IntegerField,
    DateTimeField,
    TimeField,
    SelectField,

    SubmitField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, ValidationError
)

from app import db, bcrypt
from app.models import User, Laboratorio



class UserForm(FlaskForm):
    """ Formulário para Cadastro de Usuários """
    nome = StringField("Nome", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    confirmar_senha = PasswordField(
        "Confirmar senha",
        validators=[DataRequired(),
                    EqualTo('senha', message='As senhas devem coincidir.')]
    )

    submit = SubmitField("Cadastrar")


    # Funções 'validate_<campo>' são evocadas automaticamente pelo Flask-WTF.
    def validate_email(self, email):
        """
        Verifica se o email já está cadastrado, levantando erro se positivo.
        """

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Este e-mail já está cadastrado.")
        
    
    def save(self):
        """ Salva o usuário no banco de dados. """

        # Criptografa a senha usando hash.
        senha = bcrypt.generate_password_hash(self.senha.data).decode("utf-8")
        
        # Valida se a criptografia foi realizada corretamente a partir do salt.
        if not str(senha).startswith("$2b$"):
            raise ValidationError("Falha ao criptografar senha corretamente.")
        

        try:
            """ Tenta salvar dados do usuário no banco de dados. """
            user = User(
                nome = self.nome.data,
                email = self.email.data,
                senha = senha
            )

            db.session.add(user)
            db.session.commit()


            return user
        except Exception as e:
            # Caso algo dê errado, reverta as alterações no banco e lança um erro.
            db.session.rollback()
            raise ValidationError(
                "Erro ao salvar usuário:", e
            )


# Formulário de login



class LabForm(FlaskForm):
    """ Formulário para Manipulação de Laboratórios """

    nome = StringField("Nome do laboratório", validators=[DataRequired()])
    capacidade = IntegerField("Capacidade do laboratório", validators=[DataRequired()])
    equipamentos = StringField("Equipamentos disponíveis", validators=[DataRequired()])
    abertura = TimeField("Horário de", validators=[DataRequired()])
    fechamento = TimeField("Horário de", validators=[DataRequired()])

    submit = SubmitField("Criar Laboratório")


    def save(self):
        # Salva objeto na tabela Laboratorios

        try:
            lab = Laboratorio(
                nome = self.nome.data,
                capacidade = self.capacidade.data,
                equipamentos = self.equipamentos.data,
                abertura = self.abertura.data,
                fechamento = self.fechamento.data
            )

            db.session.add(lab)
            db.session.commit()


            return lab
        except Exception as e:
            db.session.rollback()
            raise ValidationError(
                "Erro ao cadastrar laboratório:", e
            )


# TODO: Terminar depois
class SolicitacaoForm(FlaskForm):
    lab = SelectField(
        "Laboratório", coerce=int, choices=[], validators=[DataRequired()]
    )
    data_agendada = DateTimeField()
