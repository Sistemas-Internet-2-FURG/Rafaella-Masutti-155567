from flask import Flask, request, render_template, redirect, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = 'opa'


@app.route("/")
@app.route("/login", methods=['POST','GET'])
def logar():
	if 'usuarioLogado' in session:
		return redirect("/inicio")
	if request.method == 'POST':
		usuario = request.form.get('usuario')
		senha = request.form.get('senha')
		conexao = sqlite3.connect("animaisEstimacao.db")
		cursor = conexao.cursor()
		cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
		usuarioExiste = cursor.fetchone()
		if usuarioExiste != None:
			cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
			# ('senha')
			senhaDoCara = cursor.fetchone()[0]
			conexao.close()
			if senha == senhaDoCara:
				session['usuarioLogado'] = usuario
				return redirect("/inicio")
			msgErro = "Usuario ou senha incorreto(os)"
			return render_template("login.html", msgErro = msgErro)
		conexao.close()
		msgErro = "Usuario ou senha incorreto(os)"
		return render_template("login.html", msgErro = msgErro)
	else:
		return (render_template("login.html"))

@app.route("/cadastro", methods=['POST','GET'])
def cadastrar():
	if 'usuarioLogado' in session:
		return redirect("/inicio")
	if request.method == 'POST':	
		usuario = request.form.get('usuario')
		nome = request.form.get('nome')
		senha = request.form.get('senha')
		confirma = request.form.get('confirma')
		if confirma != senha:
			msgErro = "Senhas não coincidem!"
			return render_template("cadastro.html", msgErro = msgErro, dadosForm = request.form)
		conexao = sqlite3.connect("animaisEstimacao.db")
		cursor = conexao.cursor()
		cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
		usuarioExiste = cursor.fetchone()
		if usuarioExiste != None:
			msgErro = "Usuário já existe"
			conexao.close()
			return render_template("cadastro.html", msgErro = msgErro, dadosForm = request.form)
		cursor.execute("INSERT INTO usuarios (usuario,nome,senha) VALUES (?,?,?)", (usuario, nome, senha))
		conexao.commit()
		conexao.close()
		return render_template('cadastro.html', sucesso=True, dadosForm={})
	else:
		return render_template("cadastro.html", dadosForm={})

@app.route("/inicio", methods=['POST','GET'])
def inicio():
	if 'usuarioLogado' not in session:
		return redirect("/login")
	if request.method == 'POST':
		dono = session['usuarioLogado']
		foto = request.files.get('foto')
		especie = request.form.get('animal')
		nome = request.form.get('nome')
		conexao = sqlite3.connect("animaisEstimacao.db")
		cursor = conexao.cursor()
		if foto == None or foto.filename == '':
			caminho = "static/imagens/padrao.jpg"
		else:
			caminho = f"static/imagens/{foto.filename}"
			foto.save(caminho)
		cursor.execute("INSERT INTO animais (dono, foto, nome, especie) VALUES (?, ?, ?, ?)", (dono, caminho, nome, especie))
		conexao.commit()
		conexao.close()
		return redirect("/inicio")
	else:	
		usuarioLogado = session['usuarioLogado']
		conexao = sqlite3.connect("animaisEstimacao.db")
		cursor = conexao.cursor()
		cursor.execute("SELECT nome FROM usuarios WHERE usuario = ?", (usuarioLogado,))
		nomeLogado = cursor.fetchone()[0]
		cursor.execute("SELECT id,foto,nome,especie FROM animais WHERE dono = ?", (usuarioLogado,))
		#[(foto1, nome1, especie1),(foto2, nome2, especie2), ...]
		animais = cursor.fetchall()
		conexao.close()
		return render_template("inicio.html", nome = nomeLogado, animais = animais)

@app.route("/sair")
def sair():
	session.pop('usuarioLogado', None)
	return redirect("/login")

@app.route("/inicio/<id>", methods=['POST'])
def apagar(id):
	if 'usuarioLogado' not in session:
		return redirect("/login")
	id = int(id)
	conexao = sqlite3.connect("animaisEstimacao.db")
	cursor = conexao.cursor()
	cursor.execute("SELECT dono FROM animais WHERE id=?", (id,))
	dono = cursor.fetchone()[0]
	if dono == session['usuarioLogado']:
		cursor.execute("DELETE FROM animais WHERE id=?", (id,))
		conexao.commit()
	conexao.close()
	return(redirect("/inicio"))


@app.route("/inicio/editar/<id>", methods=['POST', 'GET'])
def editar(id):
	if 'usuarioLogado' not in session:
		return redirect("/login")
	if request.method == 'POST':
		foto = request.files.get('foto')
		especie = request.form.get('animal')
		nome = request.form.get('nome')
		conexao = sqlite3.connect("animaisEstimacao.db")
		cursor = conexao.cursor()
		if foto == None or foto.filename == '':
			cursor.execute("UPDATE animais SET nome=?, especie=? WHERE id=?", (nome, especie, id))
		else:
			cursor.execute("SELECT foto FROM animais WHERE id=?", (id,))
			fotoAntiga = cursor.fetchone()[0]
			caminho = f"static/imagens/{foto.filename}"
			foto.save(caminho)
			cursor.execute("UPDATE animais SET foto=?, nome=?, especie=? WHERE id=?", (caminho, nome, especie, id))
			os.remove(fotoAntiga)
		conexao.commit()
		conexao.close()
		return redirect("/inicio")
	else:
		conexao = sqlite3.connect("animaisEstimacao.db")
		cursor = conexao.cursor()
		cursor.execute("SELECT dono FROM animais WHERE id=?", (id,))
		dono = cursor.fetchone()[0]
		if dono == session['usuarioLogado']:
			cursor.execute("SELECT id, foto, nome, especie FROM animais WHERE id=?", (id,))
			editado = cursor.fetchone()
			conexao.close()
			return(render_template("editar.html", editado = editado))
		else:
			return redirect("/inicio")

if __name__ == "__main__":
	app.run(debug=True)