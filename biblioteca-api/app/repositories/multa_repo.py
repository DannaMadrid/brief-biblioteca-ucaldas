from typing import List, Optional
from app.db import memoria
from app.models.multa import Multa


class MultaRepository:
    def get_all(self) -> List[Multa]:
        return list(memoria.multas.values())

    def get_by_id(self, id: str) -> Optional[Multa]:
        return memoria.multas.get(id)

    def get_by_estudiante(self, estudiante_cod: str) -> List[Multa]:
        return [m for m in memoria.multas.values() if m.estudiante_cod == estudiante_cod]

    def get_pendientes_by_estudiante(self, estudiante_cod: str) -> List[Multa]:
        return [
            m for m in memoria.multas.values()
            if m.estudiante_cod == estudiante_cod and m.estado == "pendiente"
        ]

    def save(self, multa: Multa) -> Multa:
        memoria.multas[multa.id] = multa
        return multa

    def update(self, multa: Multa) -> Multa:
        memoria.multas[multa.id] = multa
        return multa
