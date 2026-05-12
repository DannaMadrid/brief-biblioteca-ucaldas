from datetime import date
from typing import Literal
from pydantic import BaseModel


class SolicitudReserva(BaseModel):
    id: str
    estudiante_codigo: str
    libro_codigo: str
    fecha_solicitud: date
    estado: Literal["activa", "cancelada", "atendida"] = "activa"
