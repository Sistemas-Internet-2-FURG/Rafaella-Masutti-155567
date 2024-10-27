from flask import request, jsonify, g
import src.modelos.usuario as modelos
from pydantic import ValidationError
from flask_bcrypt import Bcrypt
import src.repositories.usuario as repositories

bcrypt = Bcrypt()

def criarUsuario():
    dados = request.get_json()
    try:
        usuario = modelos.Usuario(**dados)
    except ValidationError as e:
        return jsonify({"erro":e.errors()}), 400
    usuarioDict = usuario.model_dump()
    usuarioDict["senha"] = bcrypt.generate_password_hash(usuarioDict["senha"]).decode("utf-8")
    usuarioId, erro = repositories.criarUsuario(usuarioDict)
    if erro != None: 
        if erro == 409:
            return jsonify({"erro": "Usuário já existe"}), 409
        return jsonify({"erro": erro}), 500
    return jsonify({"id": usuarioId}), 201

def buscarUsuarioLogado():
    idToken = g.user_id
    usuario, erro = repositories.buscarUsuario(idToken)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if usuario == None:
        return "", 204
    return jsonify(usuario), 200
    