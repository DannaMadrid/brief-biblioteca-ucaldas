from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.api.deps import get_libro_service
from app.api.schemas.libro_schema import LibroDetalleResponse, LibroResponse
from app.services.libro_service import LibroService

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.get("", response_model=List[LibroResponse])
def listar_libros(
    titulo: Optional[str] = Query(None),
    autor: Optional[str] = Query(None),
    disponible: Optional[bool] = Query(None),
    alta_demanda: Optional[bool] = Query(None),
    service: LibroService = Depends(get_libro_service),
):
    return service.listar_libros(titulo, autor, disponible, alta_demanda)


@router.get("/{codigo}", response_model=LibroDetalleResponse)
def obtener_libro(
    codigo: str,
    service: LibroService = Depends(get_libro_service),
):
    return service.obtener_libro_con_ejemplares(codigo)
