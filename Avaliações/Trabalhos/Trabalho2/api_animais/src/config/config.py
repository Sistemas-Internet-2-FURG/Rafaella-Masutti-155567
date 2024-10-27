from dotenv import load_dotenv
import os

load_dotenv()
nomeBanco = os.getenv("DB_NAME")
chave = os.getenv("SECRET_KEY")
debug = bool(os.getenv("DEBUG"))