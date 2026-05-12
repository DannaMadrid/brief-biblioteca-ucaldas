import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import ejemplares, estudiantes, libros, multas, prestamos, reservas
from app.core.exceptions import ConflictoDeNegocio, DatosInvalidos, EntidadNoEncontrada
from app.db.seed import cargar_datos_iniciales


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "true":
        cargar_datos_iniciales()
    yield


app = FastAPI(
    title="API Sistema de Préstamos — Biblioteca Universidad de Caldas",
    description="Gestión de préstamos, devoluciones, multas y reservas de libros.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(EntidadNoEncontrada)
async def not_found_handler(request: Request, exc: EntidadNoEncontrada):
    return JSONResponse(
        status_code=404,
        content={"error": exc.codigo_error, "mensaje": exc.mensaje},
    )


@app.exception_handler(ConflictoDeNegocio)
async def conflict_handler(request: Request, exc: ConflictoDeNegocio):
    return JSONResponse(
        status_code=409,
        content={"error": exc.codigo_error, "mensaje": exc.mensaje},
    )


@app.exception_handler(DatosInvalidos)
async def bad_request_handler(request: Request, exc: DatosInvalidos):
    return JSONResponse(
        status_code=400,
        content={"error": exc.codigo_error, "mensaje": exc.mensaje},
    )


app.include_router(libros.router)
app.include_router(ejemplares.router)
app.include_router(prestamos.router)
app.include_router(estudiantes.router)
app.include_router(multas.router)
app.include_router(reservas.router)


@app.get("/", tags=["Info"])
def root():
    return {
        "sistema": "API Biblioteca Universidad de Caldas",
        "version": "1.0.0",
        "documentacion": "/docs",
    }
