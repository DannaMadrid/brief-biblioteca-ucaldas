from datetime import date
from pydantic import BaseModel


class ReservaCreate(BaseModel):
    estudiante_codigo: str
    libro_codigo: str


class ReservaResponse(BaseModel):
    id: str
    estudiante_codigo: str
    libro_codigo: str
    fecha_solicitud: date
    estado: str
