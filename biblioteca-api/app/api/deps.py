from app.repositories.ejemplar_repo import EjemplarRepository
from app.repositories.estudiante_repo import EstudianteRepository
from app.repositories.libro_repo import LibroRepository
from app.repositories.multa_repo import MultaRepository
from app.repositories.prestamo_repo import PrestamoRepository
from app.repositories.reserva_repo import ReservaRepository
from app.services.ejemplar_service import EjemplarService
from app.services.libro_service import LibroService
from app.services.multa_service import MultaService
from app.services.prestamo_service import PrestamoService
from app.services.reserva_service import ReservaService


def get_libro_service() -> LibroService:
    return LibroService(LibroRepository(), EjemplarRepository())


def get_ejemplar_service() -> EjemplarService:
    return EjemplarService(EjemplarRepository())


def get_multa_service() -> MultaService:
    return MultaService(MultaRepository(), EstudianteRepository())


def get_prestamo_service() -> PrestamoService:
    multa_svc = MultaService(MultaRepository(), EstudianteRepository())
    return PrestamoService(
        PrestamoRepository(),
        EstudianteRepository(),
        EjemplarRepository(),
        LibroRepository(),
        multa_svc,
        ReservaRepository(),
    )


def get_reserva_service() -> ReservaService:
    return ReservaService(ReservaRepository(), EstudianteRepository(), LibroRepository())
