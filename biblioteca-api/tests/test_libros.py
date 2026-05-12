from app.db import memoria
from app.models.libro import Libro


def test_listar_libros_vacio(client):
    resp = client.get("/libros")
    assert resp.status_code == 200
    assert resp.json() == []


def test_listar_libros(client, libro_normal, libro_alta_demanda):
    resp = client.get("/libros")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filtrar_por_alta_demanda_true(client, libro_normal, libro_alta_demanda):
    resp = client.get("/libros?alta_demanda=true")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["codigo"] == "LIB-002"


def test_filtrar_por_alta_demanda_false(client, libro_normal, libro_alta_demanda):
    resp = client.get("/libros?alta_demanda=false")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["codigo"] == "LIB-001"


def test_filtrar_por_titulo(client, libro_normal, libro_alta_demanda):
    resp = client.get("/libros?titulo=Algo")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["codigo"] == "LIB-001"


def test_filtrar_por_autor(client, libro_normal, libro_alta_demanda):
    resp = client.get("/libros?autor=Stewart")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["codigo"] == "LIB-002"


def test_obtener_libro_con_ejemplares(client, libro_normal, ejemplar_normal):
    resp = client.get("/libros/LIB-001")
    assert resp.status_code == 200
    data = resp.json()
    assert data["codigo"] == "LIB-001"
    assert len(data["ejemplares"]) == 1
    assert data["ejemplares"][0]["id"] == "EJ-001"


def test_obtener_libro_no_encontrado(client):
    resp = client.get("/libros/NO-EXISTE")
    assert resp.status_code == 404
    assert resp.json()["error"] == "libro_no_encontrado"
