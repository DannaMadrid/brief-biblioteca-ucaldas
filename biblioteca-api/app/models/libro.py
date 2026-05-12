from pydantic import BaseModel


class Libro(BaseModel):
    codigo: str
    titulo: str
    autor: str
    sala: str
    alta_demanda: bool
