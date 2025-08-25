from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import User, Laboratorio
from app.forms import UserForm, LabForm


@app.route("/") #/homepage é padrão
def homepage():
    """Renderiza rota para homepage"""
    return render_template("index.html")


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



@app.route("/labs/create", methods=["GET", "POST"])
@login_required
def labs_create():
    form = LabForm()

    if form.validate_on_submit():
        lab = form.save()
        if lab:
            url_homepage = url_for('homepage')
            return (
                f"Laboratório {lab.nome} com capacidade: {lab.capacidade} foi "
                "criado com sucesso.<hr>"
                f'<a href="{url_homepage}">Voltar</a>')

    return render_template("labs/create.html", form=form)


@app.route("/labs/list", methods=["GET", "POST"])
def labs_list():
    labs = Laboratorio.query.all()

    return render_template("labs/list.html", labs=labs)


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