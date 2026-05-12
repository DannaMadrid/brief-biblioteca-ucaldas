from datetime import date, timedelta

from app.db import memoria
from app.models.multa import Multa


def _insertar_multa(multa_id="M-001", estudiante_cod="EST-001", estado="pendiente"):
    multa = Multa(
        id=multa_id,
        estudiante_cod=estudiante_cod,
        ejemplar_id="EJ-001",
        prestamo_id="P-001",
        fecha_devolucion_real=date.today(),
        dias_retraso=3,
        valor_total=6000.0,
        estado=estado,
    )
    memoria.multas[multa.id] = multa
    return multa


def test_pagar_multa_exitoso(client, estudiante_pregrado):
    _insertar_multa()
    resp = client.post("/multas/M-001/pago", json={"fecha_pago": date.today().isoformat()})
    assert resp.status_code == 200
    data = resp.json()
    assert data["estado"] == "pagada"
    assert data["fecha_pago"] == date.today().isoformat()


def test_pagar_multa_ya_pagada(client, estudiante_pregrado):
    _insertar_multa(estado="pagada")
    resp = client.post("/multas/M-001/pago", json={"fecha_pago": date.today().isoformat()})
    assert resp.status_code == 400
    assert resp.json()["error"] == "multa_ya_pagada"


def test_pagar_multa_no_encontrada(client):
    resp = client.post("/multas/NO-EXISTE/pago", json={"fecha_pago": date.today().isoformat()})
    assert resp.status_code == 404
    assert resp.json()["error"] == "multa_no_encontrada"


def test_multa_desbloqueada_permite_nuevo_prestamo(client, estudiante_pregrado, ejemplar_normal):
    from app.models.libro import Libro
    from app.models.ejemplar import Ejemplar

    # Insertar una multa pendiente → bloquea el préstamo
    _insertar_multa()
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 409

    # Pagar la multa
    client.post("/multas/M-001/pago", json={"fecha_pago": date.today().isoformat()})

    # Ahora sí puede pedir prestado
    resp = client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    assert resp.status_code == 201
