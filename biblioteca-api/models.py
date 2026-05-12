from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Libro(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str
    isbn: str
    disponible: bool = True


class LibroResponse(Libro):
    id: int


class Prestamo(BaseModel):
    id: Optional[int] = None
    id_libro: int
    id_usuario: str
    fecha_prestamo: Optional[datetime] = None
    fecha_devolución_esperada: datetime
    fecha_devolución_real: Optional[datetime] = None
    estado: str = "vigente"  # vigente, completado


class PrestamoResponse(Prestamo):
    id: int


class Devolucion(BaseModel):
    fecha_devolucion: Optional[datetime] = None
