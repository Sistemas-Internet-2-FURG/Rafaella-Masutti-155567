import jwt
from functools import wraps
from flask import request, jsonify, g
from src.config.config import chave

def autorizar(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]
        else:
            return jsonify({"erro": "Token faltando"}), 401
        try:
            payload = jwt.decode(token, chave, algorithms=["HS256"])
            g.user_id = payload.get("user_id")
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        return func(*args, **kwargs)
    return decorator