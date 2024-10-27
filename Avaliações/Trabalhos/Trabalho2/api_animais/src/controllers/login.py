from flask import request, jsonify
import src.modelos.usuario as modelos
from pydantic import ValidationError
from flask_bcrypt import Bcrypt
import src.repositories.usuario as repositories
from datetime import datetime, timedelta, timezone
import jwt
from src.config.config import chave

bcrypt = Bcrypt()

def login():
    dados = request.get_json()
    try:
        usuario = modelos.Login(**dados)
    except ValidationError as e:
        return jsonify({"erro":e.errors()}), 400
    senhaCerta, id, erro = repositories.buscarSenhaEId(usuario.usuario)
    if erro != None:
        return jsonify({"erro": erro}), 500
    if senhaCerta == None:
        return jsonify({"erro": "Usuário não encontrado"}), 401
    if bcrypt.check_password_hash(senhaCerta, usuario.senha):
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        token = jwt.encode({"user_id": id, "exp": expiration}, chave, algorithm="HS256")
        return jsonify({"token": token}), 200
    return jsonify({"erro": "Senha incorreta"}), 401