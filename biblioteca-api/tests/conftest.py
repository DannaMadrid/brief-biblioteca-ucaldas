import os

os.environ["TESTING"] = "true"  # debe estar antes del import de app

import pytest
from fastapi.testclient import TestClient

from app.db import memoria
from app.main import app
from app.models.ejemplar import Ejemplar
from app.models.estudiante import Estudiante
from app.models.libro import Libro


@pytest.fixture(autouse=True)
def reset_db():
    memoria.libros.clear()
    memoria.ejemplares.clear()
    memoria.estudiantes.clear()
    memoria.prestamos.clear()
    memoria.multas.clear()
    memoria.reservas.clear()
    yield


@pytest.fixture
def client(reset_db):
    return TestClient(app)


# ── Fixtures de datos ────────────────────────────────────────────────────────

@pytest.fixture
def libro_normal():
    libro = Libro(codigo="LIB-001", titulo="Algoritmos", autor="Cormen", sala="Sala B", alta_demanda=False)
    memoria.libros[libro.codigo] = libro
    return libro


@pytest.fixture
def libro_alta_demanda():
    libro = Libro(codigo="LIB-002", titulo="Cálculo", autor="Stewart", sala="Sala A", alta_demanda=True)
    memoria.libros[libro.codigo] = libro
    return libro


@pytest.fixture
def ejemplar_normal(libro_normal):
    ej = Ejemplar(id="EJ-001", cod_libro="LIB-001", estado="disponible")
    memoria.ejemplares[ej.id] = ej
    return ej


@pytest.fixture
def ejemplar_alta_demanda(libro_alta_demanda):
    ej = Ejemplar(id="EJ-002", cod_libro="LIB-002", estado="disponible")
    memoria.ejemplares[ej.id] = ej
    return ej


@pytest.fixture
def estudiante_pregrado():
    est = Estudiante(codigo="EST-001", nombre="Carlos Pérez", programa_academico="Ing. Sistemas", nivel_academico="pregrado")
    memoria.estudiantes[est.codigo] = est
    return est


@pytest.fixture
def estudiante_postgrado():
    est = Estudiante(codigo="EST-002", nombre="Laura Gómez", programa_academico="Maestría", nivel_academico="postgrado")
    memoria.estudiantes[est.codigo] = est
    return est
