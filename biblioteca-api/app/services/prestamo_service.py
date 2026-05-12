import uuid
from datetime import date, timedelta
from typing import List, Optional, Tuple

from app.core.exceptions import ConflictoDeNegocio, EntidadNoEncontrada
from app.models.multa import Multa
from app.models.prestamo import Prestamo
from app.repositories.ejemplar_repo import EjemplarRepository
from app.repositories.estudiante_repo import EstudianteRepository
from app.repositories.libro_repo import LibroRepository
from app.repositories.multa_repo import MultaRepository
from app.repositories.prestamo_repo import PrestamoRepository
from app.repositories.reserva_repo import ReservaRepository
from app.services.multa_service import MultaService

_LIMITE_PRESTAMOS = {"pregrado": 3, "postgrado": 5}
_DIAS_PRESTAMO = {True: 3, False: 15}  # alta_demanda → días


class PrestamoService:
    def __init__(
        self,
        prestamo_repo: PrestamoRepository,
        estudiante_repo: EstudianteRepository,
        ejemplar_repo: EjemplarRepository,
        libro_repo: LibroRepository,
        multa_service: MultaService,
        reserva_repo: ReservaRepository,
    ):
        self.prestamo_repo = prestamo_repo
        self.estudiante_repo = estudiante_repo
        self.ejemplar_repo = ejemplar_repo
        self.libro_repo = libro_repo
        self.multa_service = multa_service
        self.reserva_repo = reserva_repo

    # ── RN1 · RN2 · RN3 · RN4 · RN5 ────────────────────────────────────────
    def crear_prestamo(
        self,
        estudiante_codigo: str,
        ejemplar_id: str,
        fecha_actual: Optional[date] = None,
    ) -> Prestamo:
        if fecha_actual is None:
            fecha_actual = date.today()

        estudiante = self.estudiante_repo.get_by_codigo(estudiante_codigo)
        if not estudiante:
            raise EntidadNoEncontrada(
                f"Estudiante '{estudiante_codigo}' no encontrado.",
                "estudiante_no_encontrado",
            )

        ejemplar = self.ejemplar_repo.get_by_id(ejemplar_id)
        if not ejemplar:
            raise EntidadNoEncontrada(
                f"Ejemplar '{ejemplar_id}' no encontrado.",
                "ejemplar_no_encontrado",
            )

        libro = self.libro_repo.get_by_codigo(ejemplar.cod_libro)
        if not libro:
            raise EntidadNoEncontrada(
                f"Libro '{ejemplar.cod_libro}' no encontrado.",
                "libro_no_encontrado",
            )

        # RN1 — límite de préstamos simultáneos
        activos = self.prestamo_repo.get_activos_by_estudiante(estudiante_codigo)
        limite = _LIMITE_PRESTAMOS[estudiante.nivel_academico]
        if len(activos) >= limite:
            raise ConflictoDeNegocio(
                f"Límite de préstamos alcanzado ({limite}).",
                "limite_prestamos_alcanzado",
            )

        # RN2 — bloqueo por préstamo vencido
        for p in activos:
            if p.fecha_devolucion_esperada < fecha_actual:
                raise ConflictoDeNegocio(
                    "El estudiante tiene préstamos vencidos sin devolver.",
                    "prestamo_vencido_pendiente",
                )

        # RN3 — bloqueo por multa pendiente
        if self.multa_service.multa_repo.get_pendientes_by_estudiante(estudiante_codigo):
            raise ConflictoDeNegocio(
                "El estudiante tiene multas pendientes de pago.",
                "multa_pendiente",
            )

        # RN4 — ejemplar disponible
        if ejemplar.estado != "disponible":
            raise ConflictoDeNegocio(
                "El ejemplar no está disponible para préstamo.",
                "ejemplar_no_disponible",
            )

        # RN5 — duración según tipo de libro
        dias = _DIAS_PRESTAMO[libro.alta_demanda]
        prestamo = Prestamo(
            id=str(uuid.uuid4()),
            estudiante_cod=estudiante_codigo,
            ejemplar_id=ejemplar_id,
            fecha_prestamo=fecha_actual,
            fecha_devolucion_esperada=fecha_actual + timedelta(days=dias),
        )

        self.ejemplar_repo.update_estado(ejemplar_id, "prestado")
        return self.prestamo_repo.save(prestamo)

    # ── RN6 · RN7 ───────────────────────────────────────────────────────────
    def devolver_prestamo(
        self,
        prestamo_id: str,
        fecha_devolucion_real: date,
    ) -> Tuple[Prestamo, Optional[Multa]]:
        prestamo = self.prestamo_repo.get_by_id(prestamo_id)
        if not prestamo:
            raise EntidadNoEncontrada(
                f"Préstamo '{prestamo_id}' no encontrado.",
                "prestamo_no_encontrado",
            )

        # RN6
        if prestamo.estado == "devuelto":
            raise ConflictoDeNegocio(
                "El préstamo no puede ser devuelto porque ya fue cerrado.",
                "prestamo_no_devolvible",
            )

        devuelto = prestamo.model_copy(update={"estado": "devuelto"})
        self.prestamo_repo.update(devuelto)
        self.ejemplar_repo.update_estado(prestamo.ejemplar_id, "disponible")

        # RN7 — multa por retraso
        multa = None
        if fecha_devolucion_real > prestamo.fecha_devolucion_esperada:
            multa = self.multa_service.crear_multa(prestamo, fecha_devolucion_real)

        return devuelto, multa

    # ── RN8 ─────────────────────────────────────────────────────────────────
    def renovar_prestamo(self, prestamo_id: str, fecha_renovacion: date) -> Prestamo:
        prestamo = self.prestamo_repo.get_by_id(prestamo_id)
        if not prestamo:
            raise EntidadNoEncontrada(
                f"Préstamo '{prestamo_id}' no encontrado.",
                "prestamo_no_encontrado",
            )

        if prestamo.estado != "activo":
            raise ConflictoDeNegocio(
                "Solo se pueden renovar préstamos con estado activo.",
                "prestamo_no_renovable",
            )

        # RN8 — bloqueo si hay reservas activas para el libro
        ejemplar = self.ejemplar_repo.get_by_id(prestamo.ejemplar_id)
        if self.reserva_repo.get_activas_by_libro(ejemplar.cod_libro):
            raise ConflictoDeNegocio(
                "Hay estudiantes en lista de espera para este libro.",
                "renovacion_bloqueada",
            )

        libro = self.libro_repo.get_by_codigo(ejemplar.cod_libro)
        dias = _DIAS_PRESTAMO[libro.alta_demanda]
        renovado = prestamo.model_copy(
            update={"fecha_devolucion_esperada": fecha_renovacion + timedelta(days=dias)}
        )
        return self.prestamo_repo.update(renovado)

    # ── Consultas ────────────────────────────────────────────────────────────
    def listar_vigentes(self, estudiante_codigo: Optional[str] = None) -> List[Prestamo]:
        prestamos = self.prestamo_repo.get_all()
        activos = [p for p in prestamos if p.estado == "activo"]
        if estudiante_codigo:
            activos = [p for p in activos if p.estudiante_cod == estudiante_codigo]
        return activos

    def listar_vencidos(self, fecha_actual: Optional[date] = None) -> List[Prestamo]:
        if fecha_actual is None:
            fecha_actual = date.today()
        return [
            p for p in self.prestamo_repo.get_all()
            if p.estado == "activo" and p.fecha_devolucion_esperada < fecha_actual
        ]

    def historial_estudiante(self, estudiante_codigo: str) -> List[Prestamo]:
        if not self.estudiante_repo.exists(estudiante_codigo):
            raise EntidadNoEncontrada(
                f"Estudiante '{estudiante_codigo}' no encontrado.",
                "estudiante_no_encontrado",
            )
        return self.prestamo_repo.get_by_estudiante(estudiante_codigo)
