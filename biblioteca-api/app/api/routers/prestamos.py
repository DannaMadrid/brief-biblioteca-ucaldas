from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.api.deps import get_prestamo_service
from app.api.schemas.prestamo_schema import (
    DevolucionRequest,
    DevolucionResponse,
    PrestamoCreate,
    PrestamoResponse,
    RenovacionRequest,
)
from app.services.prestamo_service import PrestamoService

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.get("/vigentes", response_model=List[PrestamoResponse])
def listar_vigentes(
    estudiante_codigo: Optional[str] = Query(None),
    service: PrestamoService = Depends(get_prestamo_service),
):
    return service.listar_vigentes(estudiante_codigo)


@router.get("/vencidos", response_model=List[PrestamoResponse])
def listar_vencidos(
    fecha_actual: Optional[date] = Query(None),
    service: PrestamoService = Depends(get_prestamo_service),
):
    return service.listar_vencidos(fecha_actual)


@router.post("", response_model=PrestamoResponse, status_code=201)
def crear_prestamo(
    body: PrestamoCreate,
    service: PrestamoService = Depends(get_prestamo_service),
):
    return service.crear_prestamo(body.estudiante_codigo, body.ejemplar_id)


@router.post("/{id}/devolucion", response_model=DevolucionResponse)
def devolver_prestamo(
    id: str,
    body: DevolucionRequest,
    service: PrestamoService = Depends(get_prestamo_service),
):
    prestamo, multa = service.devolver_prestamo(id, body.fecha_devolucion_real)
    return {
        "prestamo": prestamo.model_dump(),
        "multa": multa.model_dump() if multa else None,
    }


@router.post("/{id}/renovacion", response_model=PrestamoResponse)
def renovar_prestamo(
    id: str,
    body: RenovacionRequest,
    service: PrestamoService = Depends(get_prestamo_service),
):
    return service.renovar_prestamo(id, body.fecha_renovacion)
