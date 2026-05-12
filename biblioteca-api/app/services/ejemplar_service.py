from typing import List, Optional
from app.models.ejemplar import Ejemplar
from app.repositories.ejemplar_repo import EjemplarRepository


class EjemplarService:
    def __init__(self, ejemplar_repo: EjemplarRepository):
        self.ejemplar_repo = ejemplar_repo

    def listar_disponibles(self, libro_codigo: Optional[str] = None) -> List[Ejemplar]:
        return self.ejemplar_repo.get_disponibles(libro_codigo)
