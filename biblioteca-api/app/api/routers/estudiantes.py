from typing import List
from fastapi import APIRouter, Depends
from app.api.deps import get_multa_service, get_prestamo_service
from app.api.schemas.multa_schema import MultaResponse
from app.api.schemas.prestamo_schema import PrestamoResponse
from app.services.multa_service import MultaService
from app.services.prestamo_service import PrestamoService

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/{codigo}/historial", response_model=List[PrestamoResponse])
def historial_prestamos(
    codigo: str,
    service: PrestamoService = Depends(get_prestamo_service),
):
    return service.historial_estudiante(codigo)


@router.get("/{codigo}/multas", response_model=List[MultaResponse])
def multas_estudiante(
    codigo: str,
    service: MultaService = Depends(get_multa_service),
):
    return service.listar_multas_estudiante(codigo)
