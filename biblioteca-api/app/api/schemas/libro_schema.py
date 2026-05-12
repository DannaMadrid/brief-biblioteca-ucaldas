from typing import List
from pydantic import BaseModel


class EjemplarEnLibro(BaseModel):
    id: str
    estado: str


class LibroResponse(BaseModel):
    codigo: str
    titulo: str
    autor: str
    sala: str
    alta_demanda: bool


class LibroDetalleResponse(LibroResponse):
    ejemplares: List[EjemplarEnLibro]
