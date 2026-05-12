from datetime import date, timedelta

import pytest

from app.db import memoria
from app.models.ejemplar import Ejemplar
from app.models.estudiante import Estudiante
from app.models.libro import Libro
from app.models.prestamo import Prestamo


# ── Helpers ──────────────────────────────────────────────────────────────────

def _agregar_libro_y_ejemplar(codigo_libro, alta_demanda=False):
    libro = Libro(codigo=codigo_libro, titulo=f"Libro {codigo_libro}", autor="Autor", sala="Sala A", alta_demanda=alta_demanda)
    ej = Ejemplar(id=f"EJ-{codigo_libro}", cod_libro=codigo_libro, estado="disponible")
    memoria.libros[libro.codigo] = libro
    memoria.ejemplares[ej.id] = ej
    return ej


def _crear_prestamo_directo(estudiante_cod, ejemplar_id, fecha_prestamo, dias_plazo):
    """Inserta un préstamo directamente en memoria para setup de tests."""
    p = Prestamo(
        id=f"P-{ejemplar_id}",
        estudiante_cod=estudiante_cod,
        ejemplar_id=ejemplar_id,
        fecha_prestamo=fecha_prestamo,
        fecha_devolucion_esperada=fecha_prestamo + timedelta(days=dias_plazo),
    )
    memoria.prestamos[p.id] = p
    memoria.ejemplares[ejemplar_id].model_copy(update={"estado": "prestado"})
    ej_actualizado = memoria.ejemplares[ejemplar_id].model_copy(update={"estado": "prestado"})
    memoria.ejemplares[ejemplar_id] = ej_actualizado
    return p


# ── Crear préstamo (happy path) ───────────────────────────────────────────────

def test_crear_prestamo_exitoso(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["estado"] == "activo"
    assert data["estudiante_cod"] == "EST-001"
    assert data["ejemplar_id"] == "EJ-001"


# ── RN5 — duración según tipo de libro ───────────────────────────────────────

def test_rn5_plazo_normal_15_dias(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 201
    data = resp.json()
    esperada = (date.today() + timedelta(days=15)).isoformat()
    assert data["fecha_devolucion_esperada"] == esperada


def test_rn5_plazo_alta_demanda_3_dias(client, estudiante_pregrado, ejemplar_alta_demanda):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-002"})
    assert resp.status_code == 201
    data = resp.json()
    esperada = (date.today() + timedelta(days=3)).isoformat()
    assert data["fecha_devolucion_esperada"] == esperada


# ── RN1 — límite de préstamos ─────────────────────────────────────────────────

def test_rn1_limite_pregrado_max_3(client, estudiante_pregrado):
    for i in range(1, 5):
        ej = _agregar_libro_y_ejemplar(f"L{i}")
        resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": ej.id})
        if i <= 3:
            assert resp.status_code == 201, f"Préstamo {i} debería crearse"
        else:
            assert resp.status_code == 409
            assert resp.json()["error"] == "limite_prestamos_alcanzado"


def test_rn1_limite_postgrado_max_5(client, estudiante_postgrado):
    for i in range(1, 7):
        ej = _agregar_libro_y_ejemplar(f"L{i}")
        resp = client.post("/prestamos", json={"estudiante_codigo": "EST-002", "ejemplar_id": ej.id})
        if i <= 5:
            assert resp.status_code == 201, f"Préstamo {i} debería crearse"
        else:
            assert resp.status_code == 409
            assert resp.json()["error"] == "limite_prestamos_alcanzado"


# ── RN2 — bloqueo por préstamo vencido ───────────────────────────────────────

def test_rn2_bloqueo_prestamo_vencido(client, estudiante_pregrado, ejemplar_normal):
    ej2 = _agregar_libro_y_ejemplar("LIB-X")
    _crear_prestamo_directo("EST-001", ej2.id, date.today() - timedelta(days=20), 15)

    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 409
    assert resp.json()["error"] == "prestamo_vencido_pendiente"


# ── RN3 — bloqueo por multa pendiente ────────────────────────────────────────

def test_rn3_bloqueo_multa_pendiente(client, estudiante_pregrado, ejemplar_normal):
    from app.models.multa import Multa
    multa = Multa(
        id="M-001",
        estudiante_cod="EST-001",
        ejemplar_id="EJ-001",
        prestamo_id="P-001",
        fecha_devolucion_real=date.today(),
        dias_retraso=3,
        valor_total=6000.0,
    )
    memoria.multas[multa.id] = multa

    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 409
    assert resp.json()["error"] == "multa_pendiente"


# ── RN4 — ejemplar no disponible ─────────────────────────────────────────────

def test_rn4_ejemplar_no_disponible(client, estudiante_pregrado, estudiante_postgrado, ejemplar_normal):
    # Primer estudiante toma el ejemplar
    client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})

    # Segundo estudiante intenta tomar el mismo
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-002", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 409
    assert resp.json()["error"] == "ejemplar_no_disponible"


# ── RN6 — devolución ─────────────────────────────────────────────────────────

def test_rn6_devolucion_exitosa(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    prestamo_id = resp.json()["id"]

    resp = client.post(f"/prestamos/{prestamo_id}/devolucion", json={"fecha_devolucion_real": date.today().isoformat()})
    assert resp.status_code == 200
    assert resp.json()["prestamo"]["estado"] == "devuelto"


def test_rn6_devolucion_ya_devuelto(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    prestamo_id = resp.json()["id"]
    client.post(f"/prestamos/{prestamo_id}/devolucion", json={"fecha_devolucion_real": date.today().isoformat()})

    resp = client.post(f"/prestamos/{prestamo_id}/devolucion", json={"fecha_devolucion_real": date.today().isoformat()})
    assert resp.status_code == 409
    assert resp.json()["error"] == "prestamo_no_devolvible"


# ── RN7 — cálculo de multa ────────────────────────────────────────────────────

def test_rn7_sin_multa_si_devuelve_a_tiempo(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    prestamo_id = resp.json()["id"]

    resp = client.post(f"/prestamos/{prestamo_id}/devolucion", json={"fecha_devolucion_real": date.today().isoformat()})
    assert resp.status_code == 200
    assert resp.json()["multa"] is None


def test_rn7_multa_correcta_por_retraso(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    prestamo_id = resp.json()["id"]
    fecha_devolucion_esperada = resp.json()["fecha_devolucion_esperada"]

    # Devuelve 5 días tarde
    tarde = (date.fromisoformat(fecha_devolucion_esperada) + timedelta(days=5)).isoformat()
    resp = client.post(f"/prestamos/{prestamo_id}/devolucion", json={"fecha_devolucion_real": tarde})
    assert resp.status_code == 200
    multa = resp.json()["multa"]
    assert multa is not None
    assert multa["dias_retraso"] == 5
    assert multa["valor_total"] == 10000.0  # 5 días × $2.000


# ── RN8 — renovación ─────────────────────────────────────────────────────────

def test_rn8_renovacion_exitosa(client, estudiante_pregrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    prestamo_id = resp.json()["id"]

    fecha_renovacion = date.today().isoformat()
    resp = client.post(f"/prestamos/{prestamo_id}/renovacion", json={"fecha_renovacion": fecha_renovacion})
    assert resp.status_code == 200
    nueva_fecha = (date.today() + timedelta(days=15)).isoformat()
    assert resp.json()["fecha_devolucion_esperada"] == nueva_fecha


def test_rn8_renovacion_bloqueada_por_reserva(client, estudiante_pregrado, estudiante_postgrado, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    prestamo_id = resp.json()["id"]

    # Otro estudiante pone una reserva activa para el mismo libro
    client.post("/reservas", json={"estudiante_codigo": "EST-002", "libro_codigo": "LIB-001"})

    resp = client.post(f"/prestamos/{prestamo_id}/renovacion", json={"fecha_renovacion": date.today().isoformat()})
    assert resp.status_code == 409
    assert resp.json()["error"] == "renovacion_bloqueada"


# ── Consultas vigentes / vencidos ────────────────────────────────────────────

def test_listar_vigentes(client, estudiante_pregrado, ejemplar_normal):
    client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    resp = client.get("/prestamos/vigentes")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_listar_vencidos(client, estudiante_pregrado, ejemplar_normal):
    # Préstamo normal se vence en 15 días → simulamos con fecha_actual = hoy+20
    client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    fecha_futura = (date.today() + timedelta(days=20)).isoformat()
    resp = client.get(f"/prestamos/vencidos?fecha_actual={fecha_futura}")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_entidad_no_encontrada_estudiante(client, ejemplar_normal):
    resp = client.post("/prestamos", json={"estudiante_codigo": "NO-EXISTE", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 404


def test_entidad_no_encontrada_ejemplar(client, estudiante_pregrado):
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "NO-EXISTE"})
    assert resp.status_code == 404
