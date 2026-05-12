from typing import Literal
from pydantic import BaseModel


class Estudiante(BaseModel):
    codigo: str
    nombre: str
    programa_academico: str
    nivel_academico: Literal["pregrado", "postgrado"]
