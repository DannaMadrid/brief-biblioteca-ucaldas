from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.api.deps import get_ejemplar_service
from app.api.schemas.ejemplar_schema import EjemplarResponse
from app.services.ejemplar_service import EjemplarService

router = APIRouter(prefix="/ejemplares", tags=["Ejemplares"])


@router.get("/disponibles", response_model=List[EjemplarResponse])
def listar_disponibles(
    libro_codigo: Optional[str] = Query(None),
    service: EjemplarService = Depends(get_ejemplar_service),
):
    return service.listar_disponibles(libro_codigo)
