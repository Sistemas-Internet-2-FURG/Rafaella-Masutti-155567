from flask import Flask
from src.config.config import porta, debug

app = Flask(__name__)

app.config["DEBUG"] = debug

from src.controllers.usuario import usuarioBp
app.register_blueprint(usuarioBp)

from src.controllers.login import loginBp
app.register_blueprint(loginBp)

from src.controllers.animal import animalBp
app.register_blueprint(animalBp)

if __name__ == "__main__":
	app.run(port=porta)