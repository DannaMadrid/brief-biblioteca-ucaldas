from app.db import memoria
from app.models.ejemplar import Ejemplar


def test_listar_disponibles_vacio(client):
    resp = client.get("/ejemplares/disponibles")
    assert resp.status_code == 200
    assert resp.json() == []


def test_listar_disponibles(client, ejemplar_normal, ejemplar_alta_demanda):
    resp = client.get("/ejemplares/disponibles")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_listar_disponibles_filtro_libro(client, ejemplar_normal, ejemplar_alta_demanda):
    resp = client.get("/ejemplares/disponibles?libro_codigo=LIB-001")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == "EJ-001"


def test_no_muestra_prestados(client, libro_normal):
    ej = Ejemplar(id="EJ-X", cod_libro="LIB-001", estado="prestado")
    memoria.ejemplares[ej.id] = ej

    resp = client.get("/ejemplares/disponibles")
    assert resp.status_code == 200
    assert resp.json() == []
