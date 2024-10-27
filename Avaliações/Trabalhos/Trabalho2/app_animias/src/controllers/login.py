from flask import Blueprint, redirect, request, render_template, make_response
import src.modelos.usuario as models
from pydantic import ValidationError
import requests
from src.config.config import apiUrl, expiracao_token

loginBp = Blueprint("login", __name__)

@loginBp.route("/")
@loginBp.route("/login", methods=['POST','GET'])
def login():
	token = request.cookies.get('token')
	if token:
		return redirect("/inicio")
	if request.method == 'POST':
		dados = request.form
		try:
			login = models.Login(**dados)
		except ValidationError:
			msgErro = "Os dados devem ser strings"
			return render_template("login.html", msgErro = msgErro)
		loginDict = login.model_dump()
		responseApi = requests.post(f"{apiUrl}/login", json=loginDict)
		if responseApi.status_code == 200:
			expiracao_cookie = expiracao_token - 60
			token = responseApi.json().get("token")
			response = make_response(redirect("/inicio"))
			response.set_cookie("token", token, httponly=True, samesite="Strict", max_age=expiracao_cookie)
			return response
		elif responseApi.status_code == 401:
			msgErro = "Usuario ou senha incorreto(os)"
			return render_template("login.html", msgErro = msgErro)
		elif responseApi.status_code == 400:
			msgErro = "Os dados devem ser strings"
			return render_template("login.html", msgErro = msgErro)
		else:
			msgErro = "Opa, ocorreu um erro em nosso servidor. Tente novamente mais tarde."
			return render_template("login.html", msgErro = msgErro)
	if request.method == 'GET':
		return (render_template("login.html"))


@loginBp.route("/sair", methods=['GET'])
def sair():
	response = redirect("/login")
	response.set_cookie("token", "", expires=0)
	return response
