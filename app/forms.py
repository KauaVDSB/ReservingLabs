from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,

    SubmitField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, ValidationError
)

from app import db, bcrypt
from app.models import User



class UserForm(FlaskForm):
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
