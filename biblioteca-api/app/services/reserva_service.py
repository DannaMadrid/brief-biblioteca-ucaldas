import uuid
from datetime import date
from typing import Optional

from app.core.exceptions import ConflictoDeNegocio, EntidadNoEncontrada
from app.models.reserva import SolicitudReserva
from app.repositories.estudiante_repo import EstudianteRepository
from app.repositories.libro_repo import LibroRepository
from app.repositories.reserva_repo import ReservaRepository


class ReservaService:
    def __init__(
        self,
        reserva_repo: ReservaRepository,
        estudiante_repo: EstudianteRepository,
        libro_repo: LibroRepository,
    ):
        self.reserva_repo = reserva_repo
        self.estudiante_repo = estudiante_repo
        self.libro_repo = libro_repo

    def crear_reserva(
        self,
        estudiante_codigo: str,
        libro_codigo: str,
        fecha_actual: Optional[date] = None,
    ) -> SolicitudReserva:
        if fecha_actual is None:
            fecha_actual = date.today()

        if not self.estudiante_repo.exists(estudiante_codigo):
            raise EntidadNoEncontrada(
                f"Estudiante '{estudiante_codigo}' no encontrado.",
                "estudiante_no_encontrado",
            )

        if not self.libro_repo.exists(libro_codigo):
            raise EntidadNoEncontrada(
                f"Libro '{libro_codigo}' no encontrado.",
                "libro_no_encontrado",
            )

        if self.reserva_repo.existe_reserva_activa(estudiante_codigo, libro_codigo):
            raise ConflictoDeNegocio(
                "El estudiante ya tiene una reserva activa para este libro.",
                "reserva_duplicada",
            )

        reserva = SolicitudReserva(
            id=str(uuid.uuid4()),
            estudiante_codigo=estudiante_codigo,
            libro_codigo=libro_codigo,
            fecha_solicitud=fecha_actual,
        )
        return self.reserva_repo.save(reserva)
