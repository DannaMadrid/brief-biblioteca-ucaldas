from typing import List, Optional
from app.core.exceptions import EntidadNoEncontrada
from app.models.libro import Libro
from app.repositories.ejemplar_repo import EjemplarRepository
from app.repositories.libro_repo import LibroRepository


class LibroService:
    def __init__(self, libro_repo: LibroRepository, ejemplar_repo: EjemplarRepository):
        self.libro_repo = libro_repo
        self.ejemplar_repo = ejemplar_repo

    def listar_libros(
        self,
        titulo: Optional[str] = None,
        autor: Optional[str] = None,
        disponible: Optional[bool] = None,
        alta_demanda: Optional[bool] = None,
    ) -> List[Libro]:
        libros = self.libro_repo.get_all()

        if titulo:
            libros = [l for l in libros if titulo.lower() in l.titulo.lower()]
        if autor:
            libros = [l for l in libros if autor.lower() in l.autor.lower()]
        if alta_demanda is not None:
            libros = [l for l in libros if l.alta_demanda == alta_demanda]
        if disponible is not None:
            resultado = []
            for libro in libros:
                ejemplares = self.ejemplar_repo.get_by_libro(libro.codigo)
                tiene_disponibles = any(e.estado == "disponible" for e in ejemplares)
                if disponible == tiene_disponibles:
                    resultado.append(libro)
            return resultado

        return libros

    def obtener_libro_con_ejemplares(self, codigo: str) -> dict:
        libro = self.libro_repo.get_by_codigo(codigo)
        if not libro:
            raise EntidadNoEncontrada(
                f"Libro con código '{codigo}' no encontrado.",
                "libro_no_encontrado",
            )
        ejemplares = self.ejemplar_repo.get_by_libro(codigo)
        return {**libro.model_dump(), "ejemplares": [e.model_dump() for e in ejemplares]}
