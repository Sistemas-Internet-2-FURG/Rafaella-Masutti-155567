from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(dotenv_path=env_path)
debug = bool(os.getenv("DEBUG"))
apiUrl = os.getenv("APIURL")
porta = int(os.getenv("PORTA"))
expiracao_token = int(os.getenv("TOKEN_EXPIRACAO"))
