from fastapi import APIRouter, Depends
from app.api.deps import get_reserva_service
from app.api.schemas.reserva_schema import ReservaCreate, ReservaResponse
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("", response_model=ReservaResponse, status_code=201)
def crear_reserva(
    body: ReservaCreate,
    service: ReservaService = Depends(get_reserva_service),
):
    return service.crear_reserva(body.estudiante_codigo, body.libro_codigo)
