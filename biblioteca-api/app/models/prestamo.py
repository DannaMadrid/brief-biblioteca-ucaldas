from datetime import date
from typing import Literal
from pydantic import BaseModel


class Prestamo(BaseModel):
    id: str
    estudiante_cod: str
    ejemplar_id: str
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    estado: Literal["activo", "devuelto"] = "activo"
