from datetime import date
from typing import Optional
from pydantic import BaseModel


class MultaResponse(BaseModel):
    id: str
    estudiante_cod: str
    ejemplar_id: str
    prestamo_id: str
    fecha_devolucion_real: date
    dias_retraso: int
    valor_total: float
    estado: str
    fecha_pago: Optional[date] = None


class PagoMultaRequest(BaseModel):
    fecha_pago: date
