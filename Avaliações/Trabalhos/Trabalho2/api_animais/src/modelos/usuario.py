from pydantic import BaseModel, Field

class Usuario(BaseModel):
    usuario : str 
    nome : str 
    senha : str

class Login(BaseModel):
    usuario : str
    senha : str 