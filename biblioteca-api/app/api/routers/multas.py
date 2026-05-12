from fastapi import APIRouter, Depends
from app.api.deps import get_multa_service
from app.api.schemas.multa_schema import MultaResponse, PagoMultaRequest
from app.services.multa_service import MultaService

router = APIRouter(prefix="/multas", tags=["Multas"])


@router.post("/{id}/pago", response_model=MultaResponse)
def pagar_multa(
    id: str,
    body: PagoMultaRequest,
    service: MultaService = Depends(get_multa_service),
):
    return service.pagar_multa(id, body.fecha_pago)
