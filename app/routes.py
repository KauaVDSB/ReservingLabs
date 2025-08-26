from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import User, Laboratorio, Solicitacao
from app.forms import UserForm, LabForm, SolicitacaoForm

def get_url_homepage():
    return url_for('homepage')

@app.route("/")
def homepage():
    """Renderiza rota para homepage"""
    if current_user:
        username = User.query.get(current_user.id).nome
        message = f', {username}'
    

    flash(f'Bem-vindo{message}', 'success')
    return render_template("index.html")


""" /AUTH/ """
@app.route("/auth/login")
def login():
    """Renderiza rota para login"""
    return render_template("auth/login.html")


@app.route("/auth/logout")
def logout():
    """ Desloga usuário a sessão """
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/auth/cadastro", methods=["GET", "POST"])
def cadastro():
    """ Renderiza rota de cadastro """
    form = UserForm()

    if form.validate_on_submit():
        user = form.save()
        if user:
            login_user(user, remember=True)
            return redirect(url_for("homepage"))
    
    return render_template("auth/cadastro.html", form=form)


""" /LABS/ """
@app.route("/labs/create", methods=["GET", "POST"])
@login_required
def labs_create():

    if not current_user.admin:
        
        return (f"Acesso negado. <hr>"
                f'<a href="{get_url_homepage()}">Voltar</a>')

    form = LabForm()

    if form.validate_on_submit():
        lab = form.save()
        if lab:
            
            return (
                f"Laboratório {lab.nome} com capacidade: {lab.capacidade} foi "
                "criado com sucesso.<hr>"
                f'<a href="{get_url_homepage()}">Voltar</a>')

    return render_template("labs/create.html", form=form)


@app.route("/labs/list", methods=["GET", "POST"])
def labs_list():
    labs = Laboratorio.query.all()

    return render_template("labs/list.html", labs=labs)


""" /SOLICITAR/ """
@app.route("/solicitar/create", methods=["GET", "POST"])
def solicitar_create():
    """
    Rota para a criação de solicitações de laboratórios.
    Somente usuários logados podem acessar.
    """

    form = SolicitacaoForm()

    # Busca lista de laboratórios para popular campo de seleção dinâmica de laboratório.
    labs = Laboratorio.query.order_by(Laboratorio.nome).all()
    form.lab.choices = [(lab.id, lab.nome) for lab in labs]

    if form.validate_on_submit():
        try:
            solicitacao = form.save()
            flash(f"Solicitação criada com sucesso para o laboratório '{solicitacao.lab.nome}'!", 'success')
            return redirect(url_for("homepage"))
        except Exception as e:
            # O formulário já lança uma ValidationError.
            flash(f"Erro ao gerar solicitação: {e}", 'danger')
            
    return render_template("solicitacoes/create.html", form=form)



""" /TEST/ """
@app.route("/tornar-admin/<int:user_id>", methods=["GET", "POST"])
@login_required
def tornar_admin(user_id):
    user = User.query.get(user_id)

    try:
        user.admin = 1
        db.session.commit()
        return "Usuário agora é admin."
    except Exception as e:
        db.session.rollback()
        return "Falha ao tornar usuário em admin:", e