from flask import Blueprint, request, render_template, redirect
import requests
from src.config.config import apiUrl
import src.modelos.animal as models
from pydantic import ValidationError
import os

animalBp = Blueprint("animal", __name__)

@animalBp.route("/inicio", methods=['POST','GET'])
def inicio():
	token = request.cookies.get("token")
	if not token:
		return redirect("/login")
	if request.method == 'POST':
		foto = request.files.get('foto')
		especie = request.form.get('animal')
		nome = request.form.get('nome')
		if foto == None or foto.filename == '':
			caminho = "static/imagens/padrao.jpg"
		else:
			caminho = f"static/imagens/{foto.filename}"
			foto.save(caminho)
		animalDict = {"foto": caminho, "especie": especie, "nome": nome}
		cabecalho = {"Authorization":f"Bearer {token}"}
		responseApi = requests.post(f"{apiUrl}/animais", headers=cabecalho, json=animalDict)
		if responseApi.status_code == 201:
			return redirect("/inicio")
		else:
			print(responseApi.json(), responseApi.status_code)
			return redirect("/inicio")
	if request.method == 'GET':	
		cabecalho = {"Authorization":f"Bearer {token}"}
		responseApi = requests.get(f"{apiUrl}/usuarios/me", headers=cabecalho)
		if responseApi.status_code == 200:
			nomeLogado = responseApi.json().get("nome")
		elif responseApi.status_code == 401:
			return redirect("/login")
		else:
			msgErro = "Ocorreu um erro inesperado"
			return render_template("login.html", msgErro = msgErro)
		responseApi = requests.get(f"{apiUrl}/animais", headers=cabecalho)
		if responseApi.status_code == 200:
			animais = responseApi.json()
		elif responseApi.status_code == 204:
			animais = []
		elif responseApi == 401:
			return redirect("/login")
		else:
			msgErro = "Ocorreu um erro inesperado"
			return render_template("login.html", msgErro = msgErro)
		return render_template("inicio.html", nome = nomeLogado, animais = animais)

@animalBp.route("/inicio/<id>", methods=['POST'])
def apagar(id):
	token = request.cookies.get("token")
	if not token:
		return redirect("/login")
	cabecalho = {"Authorization":f"Bearer {token}"}
	getAnimal = requests.get(f"{apiUrl}/animais/{id}", headers=cabecalho)
	if getAnimal.status_code == 200:
		foto = getAnimal.json()["foto"]
	else:
		print(responseApi.status_code, responseApi.json())
		return(redirect("/inicio"))
	responseApi = requests.delete(f"{apiUrl}/animais/{id}", headers=cabecalho)
	if responseApi.status_code == 200:
		if foto != "static/imagens/padrao.jpg":
			os.remove(foto)
		return redirect("/inicio")
	else:
		print(responseApi.status_code, responseApi.json())
		return(redirect("/inicio"))

@animalBp.route("/inicio/editar/<id>", methods=['POST', 'GET'])
def editar(id):
	token = request.cookies.get("token")
	if not token:
		return redirect("/login")
	cabecalho = {"Authorization":f"Bearer {token}"}
	responseApi = requests.get(f"{apiUrl}/animais/{id}", headers=cabecalho)
	if responseApi.status_code == 200:
		editado = responseApi.json()
	else:
		print(responseApi.status_code, responseApi.json())
		return redirect("/inicio")
	if request.method == 'POST':
		foto = request.files.get('foto')
		especie = request.form.get('animal')
		nome = request.form.get('nome')
		fotoAntiga = editado["foto"]
		if foto == None or foto.filename == '':
			caminho = fotoAntiga	
		else:
			caminho = f"static/imagens/{foto.filename}"
		animalDict = {"foto": caminho, "especie": especie, "nome": nome}
		responseApi = requests.put(f"{apiUrl}/animais/{id}", headers=cabecalho, json=animalDict)
		if responseApi.status_code == 204:
			if foto != None and foto.filename != '':
				foto.save(caminho)
				if fotoAntiga != "static/imagens/padrao.jpg":
					os.remove(fotoAntiga)
			return redirect("/inicio")
		else:
			print(responseApi.json(), responseApi.status_code)
			return redirect("/inicio")
	if request.method == 'GET':
		return(render_template("editar.html", editado = editado))