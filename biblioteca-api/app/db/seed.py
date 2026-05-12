from app.db import memoria
from app.models.libro import Libro
from app.models.ejemplar import Ejemplar
from app.models.estudiante import Estudiante


def cargar_datos_iniciales() -> None:
    _libros = [
        Libro(codigo="LIB-001", titulo="Cálculo Diferencial", autor="James Stewart", sala="Sala A", alta_demanda=True),
        Libro(codigo="LIB-002", titulo="Álgebra Lineal", autor="Gilbert Strang", sala="Sala A", alta_demanda=True),
        Libro(codigo="LIB-003", titulo="Introducción a la Programación", autor="Bjarne Stroustrup", sala="Sala B", alta_demanda=False),
        Libro(codigo="LIB-004", titulo="Estructuras de Datos", autor="Robert Sedgewick", sala="Sala C", alta_demanda=False),
        Libro(codigo="LIB-005", titulo="Bases de Datos", autor="Ramez Elmasri", sala="Sala B", alta_demanda=False),
    ]
    for libro in _libros:
        memoria.libros[libro.codigo] = libro

    _ejemplares = [
        Ejemplar(id="EJ-001", cod_libro="LIB-001"),
        Ejemplar(id="EJ-002", cod_libro="LIB-001"),
        Ejemplar(id="EJ-003", cod_libro="LIB-002"),
        Ejemplar(id="EJ-004", cod_libro="LIB-003"),
        Ejemplar(id="EJ-005", cod_libro="LIB-003"),
        Ejemplar(id="EJ-006", cod_libro="LIB-004"),
        Ejemplar(id="EJ-007", cod_libro="LIB-005"),
        Ejemplar(id="EJ-008", cod_libro="LIB-005"),
    ]
    for ej in _ejemplares:
        memoria.ejemplares[ej.id] = ej

    _estudiantes = [
        Estudiante(codigo="EST-001", nombre="Carlos Pérez", programa_academico="Ingeniería de Sistemas", nivel_academico="pregrado"),
        Estudiante(codigo="EST-002", nombre="Laura Gómez", programa_academico="Maestría en Matemáticas", nivel_academico="postgrado"),
        Estudiante(codigo="EST-003", nombre="Andrés Torres", programa_academico="Física", nivel_academico="pregrado"),
    ]
    for est in _estudiantes:
        memoria.estudiantes[est.codigo] = est
