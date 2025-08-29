from flask_login import current_user
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
import datetime

from app import db, bcrypt
from app.models import User, Laboratorio, Solicitacao


#--- Formulários para Autenticação
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
        """ Verifica se o email já está cadastrado. """

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
                f"Erro ao salvar usuário: {e}"
            )


class LoginForm(FlaskForm):
    """ Formulário para Login de Usuários """
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, self.senha.data):
            return user
        else:
            return False


class UserUpdateForm(FlaskForm):
    """ Formulário para Atualização de Usuários """
    nome = StringField("Nome", validators=[DataRequired()])
    email = EmailField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Nova Senha")
    confirmar_senha = PasswordField(
        "Confirme a nova senha",
        validators=[EqualTo('senha', message='As senhas devem coincidir.')]
    )
    submit = SubmitField("Atualizar")

    
    def validate_email(self, email):
        """ Verifica se o novo e-mail já está em uso por outro usuário """
        # Esta validação permite o e-mail atual do próprio usuário.
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Este e-mail já está em uso.")
            

    
    def update_user(self, user):
        user.nome = self.nome.data
        user.email = self.email.data

        if self.senha.data:
            user.senha = bcrypt.generate_password_hash(self.senha.data).decode("utf-8")

        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValidationError(f"Erro ao atualizar usuário: {e}")


# --- Formulários para Laboratórios

class LabForm(FlaskForm):
    """ Formulário para Manipulação de Laboratórios """

    nome = StringField("Nome do laboratório", validators=[DataRequired()])
    capacidade = IntegerField("Capacidade do laboratório", validators=[DataRequired()])
    equipamentos = StringField("Equipamentos disponíveis", validators=[DataRequired()])
    abertura = TimeField("Horário de", validators=[DataRequired()])
    fechamento = TimeField("Horário de", validators=[DataRequired()])

    submit = SubmitField("Criar Laboratório")


    def validate_nome(self, nome):
        """ Valida se o nome de laboratório já está sendo usado """
        lab = Laboratorio.query.filter_by(nome=nome.data).first()
        if lab:
            raise ValidationError("Já existe um laboratório com este nome.")

    def save(self):
        """ Salva objeto na tabela Laboratorios """

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
                f"Erro ao cadastrar laboratório: {e}"
            )



class LabUpdateForm(FlaskForm):
    """ Formulário para atualização de laboratórios """
    nome = StringField("Nome do laboratório", validators=[DataRequired()])
    capacidade = IntegerField("Capacidade do laboratório", validators=[DataRequired()])
    equipamentos = StringField("Equipamentos disponíveis", validators=[DataRequired()])
    abertura = TimeField("Horário de Abertura", validators=[DataRequired()])
    fechamento = TimeField("Horário de Fechamento", validators=[DataRequired()])
    submit = SubmitField("Atualizar Laboratório")

    def validate_nome(self, nome):
        """ Valida se o nome do laboratório já está em uso por outro laboratório. """
        lab = Laboratorio.query.filter_by(nome=nome.data).first()
        if lab and lab.id != self.lab_id: # Permite que o nome do laboratório atual seja o mesmo
            raise ValidationError('Já existe um laboratório com este nome.')

    def update_lab(self, lab):
        """ Atualiza os dados do laboratório no banco de dados. """
        lab.nome = self.nome.data
        lab.capacidade = self.capacidade.data
        lab.equipamentos = self.equipamentos.data
        lab.abertura = self.abertura.data
        lab.fechamento = self.fechamento.data
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValidationError(f"Erro ao atualizar laboratório: {e}")




#--- Formulários para Solicitações

class SolicitacaoForm(FlaskForm):
    lab = SelectField(
        "Laboratório", coerce=int, choices=[], validators=[DataRequired()]
    )
    # 'format' serve para que o WTForms saiba como interpretar a data do input HTML
    # 'render_kw' exibe o seletor de data e hora do navegador.
    data_agendada = DateTimeField(
        "Data Agendada",
        format='%Y-%m-%dT%H:%M', 
        validators=[DataRequired()], 
        render_kw={"type": "datetime-local"}
        )
    data_encerramento = DateTimeField(
        "Data encerramento",
        format='%Y-%m-%dT%H:%M', 
        validators=[DataRequired()], 
        render_kw={"type": "datetime-local"}
    )

    submit = SubmitField("Solicitar")


    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        
        if self.data_encerramento.data <= self.data_agendada.data:
            self.data_encerramento.errors.append(
                "O horário de encerramento deve ser posterior ao de agendamento."
            )
            return False
        
        if self.data_agendada.data < datetime.datetime.now():
            self.data_agendada.errors.append(
                "A data de agendamento não pode ser no passado."
            )
            return False
        
        lab = Laboratorio.query.get(self.lab.data)
        if lab:
            hora_agendada = self.data_agendada.data.time()
            hora_encerramento = self.data_encerramento.data.time()

            if not (lab.abertura <= hora_agendada and lab.fechamento >= hora_encerramento):
                    self.data_agendada.errors.append(
                        f"O horário de agendamento deve ser entre {lab.abertura.strftime('%H:%M')} e"
                        f"{lab.fechamento.strftime('%H:%M')}."
                    )
                    return False
            
            # Verifica se há conflitos de horários com solicitações Pendentes ou Aprovadas
            conflitos = Solicitacao.query.filter_by(id_lab=lab.id).filter(
                (Solicitacao.status == 'Pendente') | (Solicitacao.status == 'Aprovada')
            ).filter(
                (Solicitacao.data_agendada < self.data_encerramento.data) &
                (Solicitacao.data_encerramento > self.data_agendada.data)
            ).count()

            if conflitos > 0:
                self.lab.errors.append("Já existe uma solicitação para este laboratório neste horário.")
                return False
        
        return True
                            

    def save(self):

        try:
            solicitacao = Solicitacao(
                data_agendada = self.data_agendada.data,
                data_encerramento = self.data_encerramento.data,
                user = current_user,
                lab = Laboratorio.query.get(self.lab.data)
            )

            db.session.add(solicitacao)
            db.session.commit()
            return solicitacao
        except Exception as e:
            db.session.rollback()
            raise ValidationError(
                "Erro ao gerar solicitação:", e
            )

