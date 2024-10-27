from flask import Flask
from src.config.config import chave, debug

app = Flask(__name__)
app.secret_key = chave
app.config["DEBUG"] = debug

from src.rotas.usuario import usuario_bp
app.register_blueprint(usuario_bp)

from src.rotas.login import login_bp
app.register_blueprint(login_bp)

from src.rotas.animal import animal_bp
app.register_blueprint(animal_bp)

if __name__ == "__main__":
	app.run()