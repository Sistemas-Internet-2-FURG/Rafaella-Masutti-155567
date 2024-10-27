from flask import Blueprint
import src.controllers.login as controller

login_bp = Blueprint("login",__name__)

@login_bp.route("/login", methods = ("POST",))
def login():
    return controller.login()