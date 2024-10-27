from pydantic import BaseModel

class Animal(BaseModel):
    nome : str
    especie : str
    foto : str = None