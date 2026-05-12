from typing import List, Optional
from app.db import memoria
from app.models.prestamo import Prestamo


class PrestamoRepository:
    def get_all(self) -> List[Prestamo]:
        return list(memoria.prestamos.values())

    def get_by_id(self, id: str) -> Optional[Prestamo]:
        return memoria.prestamos.get(id)

    def get_by_estudiante(self, estudiante_cod: str) -> List[Prestamo]:
        return [p for p in memoria.prestamos.values() if p.estudiante_cod == estudiante_cod]

    def get_activos_by_estudiante(self, estudiante_cod: str) -> List[Prestamo]:
        return [
            p for p in memoria.prestamos.values()
            if p.estudiante_cod == estudiante_cod and p.estado == "activo"
        ]

    def save(self, prestamo: Prestamo) -> Prestamo:
        memoria.prestamos[prestamo.id] = prestamo
        return prestamo

    def update(self, prestamo: Prestamo) -> Prestamo:
        memoria.prestamos[prestamo.id] = prestamo
        return prestamo
