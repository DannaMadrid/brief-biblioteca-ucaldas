from typing import Literal
from pydantic import BaseModel


class Ejemplar(BaseModel):
    id: str
    cod_libro: str
    estado: Literal["disponible", "prestado"] = "disponible"
