import uuid
from datetime import date
from typing import List

from app.core.exceptions import DatosInvalidos, EntidadNoEncontrada
from app.models.multa import Multa
from app.models.prestamo import Prestamo
from app.repositories.estudiante_repo import EstudianteRepository
from app.repositories.multa_repo import MultaRepository

TARIFA_DIARIA = 2000.0


class MultaService:
    def __init__(self, multa_repo: MultaRepository, estudiante_repo: EstudianteRepository):
        self.multa_repo = multa_repo
        self.estudiante_repo = estudiante_repo

    def crear_multa(self, prestamo: Prestamo, fecha_devolucion_real: date) -> Multa:
        dias_retraso = (fecha_devolucion_real - prestamo.fecha_devolucion_esperada).days
        multa = Multa(
            id=str(uuid.uuid4()),
            estudiante_cod=prestamo.estudiante_cod,
            ejemplar_id=prestamo.ejemplar_id,
            prestamo_id=prestamo.id,
            fecha_devolucion_real=fecha_devolucion_real,
            dias_retraso=dias_retraso,
            valor_total=dias_retraso * TARIFA_DIARIA,
        )
        return self.multa_repo.save(multa)

    def listar_multas_estudiante(self, estudiante_codigo: str) -> List[Multa]:
        if not self.estudiante_repo.exists(estudiante_codigo):
            raise EntidadNoEncontrada(
                f"Estudiante '{estudiante_codigo}' no encontrado.",
                "estudiante_no_encontrado",
            )
        return self.multa_repo.get_by_estudiante(estudiante_codigo)

    def pagar_multa(self, multa_id: str, fecha_pago: date) -> Multa:
        multa = self.multa_repo.get_by_id(multa_id)
        if not multa:
            raise EntidadNoEncontrada(
                f"Multa '{multa_id}' no encontrada.",
                "multa_no_encontrada",
            )
        if multa.estado == "pagada":
            raise DatosInvalidos("La multa ya fue pagada.", "multa_ya_pagada")
        actualizada = multa.model_copy(update={"estado": "pagada", "fecha_pago": fecha_pago})
        return self.multa_repo.update(actualizada)
