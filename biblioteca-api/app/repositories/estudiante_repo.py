from typing import List, Optional
from app.db import memoria
from app.models.estudiante import Estudiante


class EstudianteRepository:
    def get_all(self) -> List[Estudiante]:
        return list(memoria.estudiantes.values())

    def get_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        return memoria.estudiantes.get(codigo)

    def save(self, estudiante: Estudiante) -> Estudiante:
        memoria.estudiantes[estudiante.codigo] = estudiante
        return estudiante

    def exists(self, codigo: str) -> bool:
        return codigo in memoria.estudiantes
