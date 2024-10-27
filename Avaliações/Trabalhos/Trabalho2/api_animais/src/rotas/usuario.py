from flask import Blueprint
import src.controllers.usuario as controller
from src.middlewares.aut import autorizar

usuario_bp = Blueprint("usuarios",__name__)

@usuario_bp.route("/usuarios", methods = ("POST",))
def criarUsuario():
    return controller.criarUsuario()

@usuario_bp.route("/usuarios/me", methods = ("GET",))
@autorizar
def buscarUsuarioLogado():
    return controller.buscarUsuarioLogado()
