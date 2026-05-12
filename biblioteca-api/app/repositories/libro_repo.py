from typing import List, Optional
from app.db import memoria
from app.models.libro import Libro


class LibroRepository:
    def get_all(self) -> List[Libro]:
        return list(memoria.libros.values())

    def get_by_codigo(self, codigo: str) -> Optional[Libro]:
        return memoria.libros.get(codigo)

    def save(self, libro: Libro) -> Libro:
        memoria.libros[libro.codigo] = libro
        return libro

    def exists(self, codigo: str) -> bool:
        return codigo in memoria.libros
