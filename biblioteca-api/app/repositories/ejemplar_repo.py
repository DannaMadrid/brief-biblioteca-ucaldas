from typing import List, Optional
from app.db import memoria
from app.models.ejemplar import Ejemplar


class EjemplarRepository:
    def get_all(self) -> List[Ejemplar]:
        return list(memoria.ejemplares.values())

    def get_by_id(self, id: str) -> Optional[Ejemplar]:
        return memoria.ejemplares.get(id)

    def get_by_libro(self, cod_libro: str) -> List[Ejemplar]:
        return [e for e in memoria.ejemplares.values() if e.cod_libro == cod_libro]

    def get_disponibles(self, cod_libro: Optional[str] = None) -> List[Ejemplar]:
        result = [e for e in memoria.ejemplares.values() if e.estado == "disponible"]
        if cod_libro:
            result = [e for e in result if e.cod_libro == cod_libro]
        return result

    def save(self, ejemplar: Ejemplar) -> Ejemplar:
        memoria.ejemplares[ejemplar.id] = ejemplar
        return ejemplar

    def update_estado(self, id: str, estado: str) -> Optional[Ejemplar]:
        ejemplar = memoria.ejemplares.get(id)
        if not ejemplar:
            return None
        actualizado = ejemplar.model_copy(update={"estado": estado})
        memoria.ejemplares[id] = actualizado
        return actualizado
