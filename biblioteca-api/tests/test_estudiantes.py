from datetime import date, timedelta

from app.db import memoria
from app.models.multa import Multa
from app.models.prestamo import Prestamo


def test_historial_estudiante(client, estudiante_pregrado, ejemplar_normal):
    client.post("/prestamos", json={"estudiante_codigo": "EST-001", "ejemplar_id": "EJ-001"})
    resp = client.get("/estudiantes/EST-001/historial")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_historial_estudiante_no_encontrado(client):
    resp = client.get("/estudiantes/NO-EXISTE/historial")
    assert resp.status_code == 404


def test_historial_vacio(client, estudiante_pregrado):
    resp = client.get("/estudiantes/EST-001/historial")
    assert resp.status_code == 200
    assert resp.json() == []


def test_multas_estudiante(client, estudiante_pregrado):
    multa = Multa(
        id="M-001",
        estudiante_cod="EST-001",
        ejemplar_id="EJ-001",
        prestamo_id="P-001",
        fecha_devolucion_real=date.today(),
        dias_retraso=2,
        valor_total=4000.0,
    )
    memoria.multas[multa.id] = multa

    resp = client.get("/estudiantes/EST-001/multas")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["valor_total"] == 4000.0


def test_multas_estudiante_no_encontrado(client):
    resp = client.get("/estudiantes/NO-EXISTE/multas")
    assert resp.status_code == 404
