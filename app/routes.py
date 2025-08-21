from flask import render_template

from app import app


@app.route("/")
def homepage():
    """Renderiza rota para homepage"""
    return render_template("index.html")


@app.route("/login")
def login():
    """Renderiza rota para login"""
    return render_template("auth/login.html")
