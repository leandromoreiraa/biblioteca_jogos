from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogo
from dao import JogoDao, UsuarioDao
from utilitarios import deleta_arquivo, recupera_imagem
from jogoteca import db, app
import time

#criar o jogodao e usuariodao e passar a isntancia do mysql que é o db
jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista_de_jogos = jogo_dao.listar()
    return render_template("lista.html", titulo ="𝔹𝕚𝕓𝕝𝕚𝕠𝕥𝕖𝕔𝕒 𝕕𝕖 𝕁𝕠𝕘𝕠𝕤", jogos=lista_de_jogos)

@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    return render_template("novo.html", titulo ="𝕀𝕟𝕤𝕚𝕣𝕒 𝕠 𝕁𝕠𝕘𝕠")


@app.route("/criar", methods=["POST",])
def create():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)

#fazendo upload da capa do jogo após ele ser salvo
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    flash("Jogo {} Cadastrado Com Sucesso.".format(nome))
    return redirect(url_for("index"))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo=f'𝔸𝕝𝕥𝕖𝕣𝕒𝕔̧𝕠̃𝕖𝕤 𝔻𝕠 𝕁𝕠𝕘𝕠:  {jogo.nome}', jogo=jogo,
                                capa_jogo = nome_imagem)



@app.route("/atualizar", methods=["POST",])
def atualizar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    jogo = Jogo(nome, categoria, console, id=request.form["id"])
    jogo_dao.salvar(jogo)

    arquivo = request.files["arquivo"]
    upload = app.config['UPLOAD_PATH']
    timestamp = time.time()
    #deletar a capa atual
    deleta_arquivo(jogo.id)
    #gerar arquivo novo, ou nesse caso a capa
    arquivo.save(f"{upload}/capa{jogo.id}-{timestamp}.jpg")
    flash("As Informações do Jogo foram Atualizadas com Sucesso.")
    return redirect(url_for("index"))




@app.route("/deletar/<int:id>")
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    jogo_dao.deletar(id)
    flash("Jogo Removido Com Sucesso.")
    return redirect(url_for("index"))


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=["POST",])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form["usuario"])
    if usuario:
        if usuario.senha == request.form["senha"]:
            session["usuario_logado"] = usuario.id
            flash(f"Seja Bem Vindo(a) ao Sistema Sr(a): {usuario.nome}")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
        elif usuario.senha != request.form["senha"]:
            flash("Senha Incorreta, Tente Novamente.")
            return redirect(url_for("login"))
    else:
        flash("Usuário Informado não possui Acesso ao Sistema, favor entrar em contato com o Administrador.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Nenhum Usuário Logado.")
    return redirect(url_for("login"))

@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory("uploads", nome_arquivo)