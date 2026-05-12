from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.api.schemas.multa_schema import MultaResponse


class PrestamoCreate(BaseModel):
    estudiante_codigo: str
    ejemplar_id: str


class DevolucionRequest(BaseModel):
    fecha_devolucion_real: date


class RenovacionRequest(BaseModel):
    fecha_renovacion: date


class PrestamoResponse(BaseModel):
    id: str
    estudiante_cod: str
    ejemplar_id: str
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    estado: str


class DevolucionResponse(BaseModel):
    prestamo: PrestamoResponse
    multa: Optional[MultaResponse] = None
