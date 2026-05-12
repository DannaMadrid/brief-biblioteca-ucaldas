from typing import Dict
from app.models.libro import Libro
from app.models.ejemplar import Ejemplar
from app.models.estudiante import Estudiante
from app.models.prestamo import Prestamo
from app.models.multa import Multa
from app.models.reserva import SolicitudReserva

libros: Dict[str, Libro] = {}
ejemplares: Dict[str, Ejemplar] = {}
estudiantes: Dict[str, Estudiante] = {}
prestamos: Dict[str, Prestamo] = {}
multas: Dict[str, Multa] = {}
reservas: Dict[str, SolicitudReserva] = {}
