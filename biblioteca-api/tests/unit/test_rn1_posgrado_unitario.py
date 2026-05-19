"""
Test unitario puro — RN1: límite de préstamos simultáneos para estudiantes de postgrado.

Estrategia de aislamiento:
    Se instancia PrestamoService directamente (sin TestClient ni HTTP).
    Los 6 repositorios se reemplazan con unittest.mock.MagicMock.
    No se toca la base de datos en memoria (memoria.py) en ningún momento.
    Resultado: cada test corre en < 10 ms y no depende de estado global.

Nota de adaptación al stack real:
    El enunciado del taller usa "posgrado" (referencia TypeScript).
    El modelo Python real (app/models/estudiante.py) define el campo como
    Literal["pregrado", "postgrado"] — se usa "postgrado" en todos los tests.
"""
import os

os.environ["TESTING"] = "true"  # evita que app/db/seed.py cargue datos

from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest

from app.core.exceptions import ConflictoDeNegocio
from app.models.ejemplar import Ejemplar
from app.models.estudiante import Estudiante
from app.models.libro import Libro
from app.models.prestamo import Prestamo
from app.services.prestamo_service import PrestamoService


# ── Helpers de construcción ──────────────────────────────────────────────────

def _prestamos_activos(n: int) -> list:
    """
    Devuelve una lista de n objetos Prestamo con:
    - fechas de devolución en el futuro  → RN2 (vencidos) no se dispara
    - estado "activo"
    """
    hoy = date.today()
    return [
        Prestamo(
            id=f"P-MOCK-{i:02d}",
            estudiante_cod="EST-PG",
            ejemplar_id=f"EJ-MOCK-{i:02d}",
            fecha_prestamo=hoy - timedelta(days=i),
            fecha_devolucion_esperada=hoy + timedelta(days=10),
            estado="activo",
        )
        for i in range(1, n + 1)
    ]


def _build_service(activos_existentes: list) -> PrestamoService:
    """
    Construye un PrestamoService con todos sus colaboradores mockeados.
    Los mocks se configuran para representar un escenario sin bloqueos
    adicionales (sin multas, ejemplar disponible, libro normal).
    """
    # ── Datos de dominio que los mocks retornarán ────────────────────────────
    estudiante = Estudiante(
        codigo="EST-PG",
        nombre="Laura Gómez",
        programa_academico="Maestría en Sistemas",
        nivel_academico="postgrado",   # valor real del Literal en el modelo
    )
    ejemplar = Ejemplar(
        id="EJ-NEW",
        cod_libro="LIB-001",
        estado="disponible",
    )
    libro = Libro(
        codigo="LIB-001",
        titulo="Estructuras de Datos Avanzadas",
        autor="Autor Test",
        sala="Sala B",
        alta_demanda=False,  # plazo normal: 15 días
    )

    # ── Repositorios mockeados ────────────────────────────────────────────────
    prestamo_repo  = MagicMock()
    estudiante_repo = MagicMock()
    ejemplar_repo  = MagicMock()
    libro_repo     = MagicMock()
    reserva_repo   = MagicMock()
    multa_service  = MagicMock()

    # ── Configuración de retornos ─────────────────────────────────────────────
    estudiante_repo.get_by_codigo.return_value  = estudiante
    ejemplar_repo.get_by_id.return_value        = ejemplar
    libro_repo.get_by_codigo.return_value       = libro

    # Lista de activos que determina si RN1 bloquea o no
    prestamo_repo.get_activos_by_estudiante.return_value = activos_existentes

    # Sin multas pendientes → RN3 no bloquea
    multa_service.multa_repo.get_pendientes_by_estudiante.return_value = []

    # save devuelve el mismo objeto que recibe (comportamiento real)
    prestamo_repo.save.side_effect = lambda p: p

    return PrestamoService(
        prestamo_repo=prestamo_repo,
        estudiante_repo=estudiante_repo,
        ejemplar_repo=ejemplar_repo,
        libro_repo=libro_repo,
        multa_service=multa_service,
        reserva_repo=reserva_repo,
    )


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestRN1PostgradoLimitePrestamos:
    """
    Verifica la RN1 para el nivel académico 'postgrado' (límite = 5).

    Scope: únicamente la lógica de negocio en PrestamoService.crear_prestamo.
    Ningún test de esta clase abre una conexión HTTP ni modifica memoria.py.
    """

    def test_quinto_prestamo_se_permite(self):
        """
        Happy path del límite: con 4 préstamos activos el quinto se otorga.

        Verifica que el servicio retorna un Prestamo válido y que
        prestamo_repo.save() fue invocado exactamente una vez.
        """
        service = _build_service(activos_existentes=_prestamos_activos(4))

        resultado = service.crear_prestamo(
            estudiante_codigo="EST-PG",
            ejemplar_id="EJ-NEW",
            fecha_actual=date.today(),
        )

        assert resultado is not None, "El servicio debe retornar un Prestamo"
        assert resultado.estado == "activo"
        assert resultado.estudiante_cod == "EST-PG"
        assert resultado.ejemplar_id == "EJ-NEW"

        # Confirmar que se persistió
        service.prestamo_repo.save.assert_called_once()

    def test_sexto_prestamo_lanza_conflicto_de_negocio(self):
        """
        RN1 — límite postgrado: el sexto préstamo debe lanzar ConflictoDeNegocio
        con codigo_error == 'limite_prestamos_alcanzado'.

        Con 5 activos existentes, len(activos) >= 5 → True → excepción esperada.
        """
        service = _build_service(activos_existentes=_prestamos_activos(5))

        with pytest.raises(ConflictoDeNegocio) as exc_info:
            service.crear_prestamo(
                estudiante_codigo="EST-PG",
                ejemplar_id="EJ-NEW",
                fecha_actual=date.today(),
            )

        assert exc_info.value.codigo_error == "limite_prestamos_alcanzado", (
            f"Se esperaba 'limite_prestamos_alcanzado', "
            f"se obtuvo '{exc_info.value.codigo_error}'"
        )
        # El mensaje debe mencionar el límite numérico (5)
        assert "5" in exc_info.value.mensaje, (
            f"El mensaje de error debería incluir el límite '5': '{exc_info.value.mensaje}'"
        )
        # save NO debe haberse llamado: no se crea ningún préstamo
        service.prestamo_repo.save.assert_not_called()


"""
──────────────────────────────────────────────────────────────────────────────
REFLEXIÓN — ¿Por qué este test sería más lento o imposible de escribir en v1?
──────────────────────────────────────────────────────────────────────────────

PROBLEMA 1 — Sin capa de servicio inyectable
    v1 no tiene PrestamoService. Toda la lógica vive dentro del handler del
    endpoint en main.py. No existe punto de entrada para instanciar la
    "lógica de negocio" sin el framework HTTP alrededor.

PROBLEMA 2 — Sin repositorios inyectables
    v1 accede directamente a estructuras de datos globales (listas/dicts en
    main.py o models.py). No hay forma de reemplazar esa fuente de datos con
    un MagicMock. Para simular "5 préstamos activos" habría que escribir
    directamente en la variable global, lo que hace los tests dependientes
    del orden de ejecución.

PROBLEMA 3 — RN1 no existe en v1
    v1 no verifica el tipo de estudiante ni aplica límites de préstamos.
    Antes de poder probar la regla, habría que implementarla, y al hacerlo
    dentro del handler seguiría siendo difícil de aislar.

PROBLEMA 4 — Ciclo de test en v1 (estimado)
    a) Levantar uvicorn (~ 1-2 segundos de startup)
    b) Insertar 5 préstamos vía 5 POST HTTP
    c) Intentar el 6to POST y verificar respuesta
    d) Limpiar estado entre tests (reiniciar servidor o vaciar globales)
    → Cada escenario: ~ 3-5 segundos. Suite completa: minutos.
    → Este test unitario corre en < 10 ms.

CONCLUSIÓN
    La separación en capas (PrestamoService + repositorios inyectables) no
    es complejidad extra — es exactamente lo que hace posible este test.
    El diseño para testabilidad es una decisión arquitectónica, no estética.
──────────────────────────────────────────────────────────────────────────────
"""
