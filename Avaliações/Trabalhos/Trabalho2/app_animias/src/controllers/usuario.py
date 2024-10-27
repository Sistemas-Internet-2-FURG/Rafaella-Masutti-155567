from flask import Blueprint, request, render_template, redirect
import src.modelos.usuario as models
from pydantic import ValidationError
from src.config.config import apiUrl
import requests

usuarioBp = Blueprint("usuario", __name__)

@usuarioBp.route("/cadastro", methods=['POST','GET'])
def cadastro():
	token = request.cookies.get("token")
	if token:
		return redirect("/inicio")
	if request.method == 'POST':
		dados = request.form	
		try:
			usuario = models.Usuario(**dados)
		except ValidationError:
			msgErro = "Senhas não coincidem!"
			return render_template("cadastro.html", msgErro = msgErro, dadosForm = dados)
		dadosDict = usuario.model_dump()
		respostaApi = requests.post(f"{apiUrl}/usuarios", json=dadosDict)
		if respostaApi.status_code == 201:
			return render_template('cadastro.html', sucesso=True, dadosForm={})
		elif respostaApi.status_code == 409:
			msgErro = "Usuário já existe"
			return render_template("cadastro.html", msgErro = msgErro, dadosForm = dados)
		elif respostaApi.status_code == 400:
			msgErro = "Preencha os dados corretamente!"
			return render_template("cadastro.html", msgErro = msgErro, dadosForm = dados)
		else:
			msgErro = "Opa, correu um erro em nosso servidor. Tente novamente mais tarde."
			return render_template("cadastro.html", msgErro = msgErro, dadosForm = dados)
	if request.method == 'GET':
		return render_template("cadastro.html", dadosForm={})	