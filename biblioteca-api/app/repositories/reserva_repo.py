from typing import List, Optional
from app.db import memoria
from app.models.reserva import SolicitudReserva


class ReservaRepository:
    def get_all(self) -> List[SolicitudReserva]:
        return list(memoria.reservas.values())

    def get_by_id(self, id: str) -> Optional[SolicitudReserva]:
        return memoria.reservas.get(id)

    def get_activas_by_libro(self, libro_codigo: str) -> List[SolicitudReserva]:
        return [
            r for r in memoria.reservas.values()
            if r.libro_codigo == libro_codigo and r.estado == "activa"
        ]

    def get_by_estudiante(self, estudiante_codigo: str) -> List[SolicitudReserva]:
        return [r for r in memoria.reservas.values() if r.estudiante_codigo == estudiante_codigo]

    def existe_reserva_activa(self, estudiante_codigo: str, libro_codigo: str) -> bool:
        return any(
            r for r in memoria.reservas.values()
            if r.estudiante_codigo == estudiante_codigo
            and r.libro_codigo == libro_codigo
            and r.estado == "activa"
        )

    def save(self, reserva: SolicitudReserva) -> SolicitudReserva:
        memoria.reservas[reserva.id] = reserva
        return reserva

    def update(self, reserva: SolicitudReserva) -> SolicitudReserva:
        memoria.reservas[reserva.id] = reserva
        return reserva
