from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import User, Laboratorio, Solicitacao
from app.forms import UserForm, LabForm, SolicitacaoForm, LoginForm, UserUpdateForm



@app.route("/") #/homepage é padrão
def homepage():
    """ Renderiza rota para homepage """

    labs_total = Laboratorio.query.count()
    labs_disponiveis = Laboratorio.query.filter_by(status='Disponível').count()
    solicitacoes_pendentes = Solicitacao.query.filter_by(status='Pendente').count()
    labs_agendados = Laboratorio.query.all()


    return render_template(
        "index.html",
        labs_total=labs_total,
        labs_disponiveis=labs_disponiveis,
        solicitacoes_pendentes=solicitacoes_pendentes,
        labs=labs_agendados
    )


""" /AUTH/ """
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    """ Renderiza rota para login de usuários """
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            flash(f'Bem-vindo, {user.nome}!', 'success')
            return redirect(url_for("homepage"))
        else:
            flash('Login inválido. Verifique seu e-mail e senha.', 'danger')

    return render_template("auth/login.html", form=form)


@app.route("/auth/logout")
@login_required
def logout():
    """ Desloga usuário a sessão """
    logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for("homepage"))


@app.route("/auth/cadastro", methods=["GET", "POST"])
@login_required
def cadastro():
    """ Renderiza rota de cadastro """
    if not current_user.admin:
        flash('Acesso negado. Apenas administradores podem cadastrar novos usuários.', 'danger')
        return redirect(url_for("homepage"))
    
    form = UserForm()

    if form.validate_on_submit():
        try:
            form.save()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for("homepage"))
        except Exception as e:
            flash(f'Erro no cadastro: {e}', 'danger')
            
    
    return render_template("auth/cadastro.html", form=form)


@app.route("/auth/profile/update", methods=["GET", "POST"])
@login_required
def update_profile():
    """ Rota para atualizar os dados do usuário logado. """
    form = UserUpdateForm()

    if form.validate_on_submit():
        if form.update_user(current_user):
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for("homepage"))
        else:
            flash('Erro ao atualizar perfil. Verifique os dados e tente novamente.', 'danger')

    elif request.method == 'GET':
        form.nome.data = current_user.nome
        form.email.data = current_user.email    
    return render_template("auth/update.html", form=form)


""" /LABS/ """
@app.route("/labs/create", methods=["GET", "POST"])
@login_required
def labs_create():

    if not current_user.admin:
        flash('Acesso negado. Apenas administradores podem criar laboratórios.', 'danger')
        return redirect(url_for("homepage"))

    form = LabForm()
    if form.validate_on_submit():
        try:
            lab = form.save()
            flash(f"Laboratório '{lab.nome}' criado com sucesso!", 'success')
            return redirect(url_for("homepage")) # Redireciona para a homepage
        except Exception as e:
            flash(f"Erro ao criar laboratório: {e}", 'danger')

    return render_template("labs/create.html", form=form)


@app.route("/labs/list", methods=["GET", "POST"])
def labs_list():
    labs = Laboratorio.query.all()

    return render_template("labs/list.html", labs=labs)


#TODO: update lab

@app.route("/labs/delete/<int:lab_id>", methods=["GET", "POST"])
@login_required
def labs_delete(lab_id):
    if not current_user.admin:
        flash('Acesso negado. Apenas administradores podem deletar laboratórios.', 'danger')
        return redirect(url_for("homepage"))

    lab = Laboratorio.query.get(lab_id)
    if not lab:
        flash("Laboratório não encontrado.", "danger")
        return redirect(url_for("homepage"))

    try:
        db.session.delete(lab)
        db.session.commit()
        flash(f"Laboratório {lab.nome} deletado com sucesso.", 'success')
        return redirect(url_for("homepage"))
    except Exception as e:
        db.session.rollback()
        flash(f"Falha ao deletar laboratório: {e}", 'danger')
        return redirect(url_for("homepage"))


""" /SOLICITAR/ """
@app.route("/solicitar/create", methods=["GET", "POST"])
@login_required
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


@app.route("/solicitar/list")
def solicitar_list():
    solicitacoes = Solicitacao.query.all()

    return render_template("solicitacoes/list.html", solicitacoes=solicitacoes)


@app.route("/solicitar/delete/<int:solicitacao_id>", methods=["GET", "POST"])
@login_required
def solicitar_delete(solicitacao_id):
    solicitacao = Solicitacao.query.get(solicitacao_id)
    if not solicitacao:
        flash("Solicitação não encontrada.", "danger")
        return redirect(url_for("homepage"))
    
    if solicitacao.user != current_user or not current_user.admin:
        flash("Acesso negado. Você não fez esta solicitação ou não é admin.", "danger")
        return redirect(url_for("homepage"))
    

    try:
        db.session.delete(solicitacao)
        db.session.commit()
        flash(f"Solicitação {solicitacao_id} para o laboratório '{solicitacao.lab.nome}' deletada com sucesso.", 'success')
        return redirect(url_for("homepage"))
    except Exception as e:
        db.session.rollback()
        flash(f"Falha ao deletar a solicitação: {e}", 'danger')
        return redirect(url_for("homepage"))



""" /ADMIN/ """
@app.route("/admin/alter/<int:user_id>", methods=["GET", "POST"])
@login_required
def admin_alter(user_id):
    if not current_user.admin:
        flash('Acesso negado. Apenas administradores podem alterar privilégios.', 'danger')
        return redirect(url_for("homepage"))
    
    user = User.query.get(user_id)
    if user:
        try:
            user.admin = 1
            db.session.commit()
            flash(f"Usuário '{user.nome}' agora é admin.", 'success')
            return redirect(url_for("homepage"))
        except Exception as e:
            db.session.rollback()
            flash(f"Falha ao tornar usuário em admin: {e}", 'danger')
            return redirect(url_for("homepage"))
    else:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("homepage"))

