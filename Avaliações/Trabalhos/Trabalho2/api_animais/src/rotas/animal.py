from flask import Blueprint
import src.controllers.animal as controller
from src.middlewares.aut import autorizar


animal_bp = Blueprint("animal",__name__)

@animal_bp.route("/animais", methods = ("POST",))
@autorizar
def criarAnimal():
    return controller.criarAnimal()

@animal_bp.route("/animais", methods = ("GET",))
@autorizar
def buscarAnimais():
    return controller.buscarAnimais()

@animal_bp.route("/animais/<id>", methods = ("GET",))
@autorizar
def buscarAnimal(id):
    return controller.buscarAnimal(id)

@animal_bp.route("/animais/<id>", methods = ("PUT",))
@autorizar
def editarAnimal(id):
    return controller.editarAnimal(id)

@animal_bp.route("/animais/<id>", methods = ("DELETE",))
@autorizar
def apagarAnimal(id):
    return controller.apagarAnimal(id)
