from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel


class Multa(BaseModel):
    id: str
    estudiante_cod: str
    ejemplar_id: str
    prestamo_id: str
    fecha_devolucion_real: date
    dias_retraso: int
    valor_total: float
    estado: Literal["pendiente", "pagada"] = "pendiente"
    fecha_pago: Optional[date] = None
