from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import User
from app.forms import UserForm


@app.route("/")
def homepage():
    """Renderiza rota para homepage"""
    return render_template("index.html")


@app.route("/login")
def login():
    """Renderiza rota para login"""
    return render_template("auth/login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """ Renderiza rota de cadastro """
    form = UserForm()

    if form.validate_on_submit():
        user = form.save()
        if user:
            login_user(user, remember=True)
            return redirect(url_for("homepage"))
    
    return render_template("auth/cadastro.html", form=form)



@app.route("/tornar-admin/<int:user_id>", methods=["GET", "POST"])
def tornar_admin(user_id):
    user = User.query.get(user_id)

    try:
        user.admin = 1
        db.session.commit()
        return "Usuário agora é admin."
    except Exception as e:
        db.session.rollback()
        return "Falha ao tornar usuário em admin:", e