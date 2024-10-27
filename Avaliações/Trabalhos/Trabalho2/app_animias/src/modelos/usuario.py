from pydantic import BaseModel, Field, model_validator

class Usuario(BaseModel):
    usuario : str
    nome : str
    senha : str
    confirma : str
    @model_validator(mode="after")
    def confirmaSenha(cls, values):
        if values.senha != values.confirma:
            raise ValueError("Senhas não coincidem")
        return values

class Login(BaseModel):
    usuario : str
    senha : str 