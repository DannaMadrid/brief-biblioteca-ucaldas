from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from datetime import datetime
from models import Libro, LibroResponse, Prestamo, PrestamoResponse, Devolucion

app = FastAPI(
    title="API Biblioteca Universitaria",
    description="API para gestionar préstamos y devoluciones de libros",
    version="1.0.0"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos en memoria
libros_db: Dict[int, dict] = {
    1: {
        "id": 1,
        "titulo": "Python 101",
        "autor": "Guido van Rossum",
        "isbn": "ISBN-001",
        "disponible": True
    },
    2: {
        "id": 2,
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "isbn": "ISBN-002",
        "disponible": True
    },
    3: {
        "id": 3,
        "titulo": "Design Patterns",
        "autor": "Gang of Four",
        "isbn": "ISBN-003",
        "disponible": False
    }
}

prestamos_db: Dict[int, dict] = {}

# Contadores para IDs
libro_id_counter = 4
prestamo_id_counter = 1


# ==================== ENDPOINTS PARA LIBROS ====================

@app.get("/libros", response_model=List[LibroResponse], tags=["Libros"])
def listar_libros(disponible: Optional[bool] = None):
    """
    Listar todos los libros en la biblioteca.
    
    Parámetros opcionales:
    - disponible: filtrar por disponibilidad (true/false)
    """
    libros_list = list(libros_db.values())
    
    if disponible is not None:
        libros_list = [libro for libro in libros_list if libro["disponible"] == disponible]
    
    return libros_list


@app.get("/libros/{libro_id}", response_model=LibroResponse, tags=["Libros"])
def obtener_libro(libro_id: int):
    """Obtener detalles de un libro específico"""
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {libro_id} no encontrado"
        )
    return libros_db[libro_id]


@app.post("/libros", response_model=LibroResponse, status_code=status.HTTP_201_CREATED, tags=["Libros"])
def crear_libro(libro: Libro):
    """Crear un nuevo libro en la biblioteca"""
    global libro_id_counter
    
    # Verificar que el ISBN sea único
    for existing_libro in libros_db.values():
        if existing_libro["isbn"] == libro.isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un libro con ISBN {libro.isbn}"
            )
    
    nuevo_libro = {
        "id": libro_id_counter,
        "titulo": libro.titulo,
        "autor": libro.autor,
        "isbn": libro.isbn,
        "disponible": True
    }
    
    libros_db[libro_id_counter] = nuevo_libro
    libro_id_counter += 1
    
    return nuevo_libro


# ==================== ENDPOINTS PARA PRÉSTAMOS ====================

@app.get("/prestamos", response_model=List[PrestamoResponse], tags=["Préstamos"])
def listar_prestamos_vigentes(estado: Optional[str] = "vigente"):
    """
    Listar préstamos vigentes o completados.
    
    Parámetros opcionales:
    - estado: 'vigente' o 'completado' (por defecto 'vigente')
    """
    prestamos_list = list(prestamos_db.values())
    
    if estado:
        prestamos_list = [p for p in prestamos_list if p["estado"] == estado]
    
    return prestamos_list


@app.get("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos"])
def obtener_prestamo(prestamo_id: int):
    """Obtener detalles de un préstamo específico"""
    if prestamo_id not in prestamos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con ID {prestamo_id} no encontrado"
        )
    return prestamos_db[prestamo_id]


@app.post("/prestamos", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED, tags=["Préstamos"])
def crear_prestamo(prestamo: Prestamo):
    """
    Crear un nuevo préstamo de libro.
    
    Requerimientos:
    - El libro debe existir
    - El libro debe estar disponible
    - La fecha de devolución esperada debe ser después de hoy
    """
    global prestamo_id_counter
    
    # Validar que el libro existe
    if prestamo.id_libro not in libros_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {prestamo.id_libro} no encontrado"
        )
    
    # Validar que el libro está disponible
    if not libros_db[prestamo.id_libro]["disponible"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El libro con ID {prestamo.id_libro} no está disponible"
        )
    
    # Validar fecha de devolución
    if prestamo.fecha_devolución_esperada <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de devolución esperada debe ser en el futuro"
        )
    
    # Crear el préstamo
    nuevo_prestamo = {
        "id": prestamo_id_counter,
        "id_libro": prestamo.id_libro,
        "id_usuario": prestamo.id_usuario,
        "fecha_prestamo": datetime.now(),
        "fecha_devolución_esperada": prestamo.fecha_devolución_esperada,
        "fecha_devolución_real": None,
        "estado": "vigente"
    }
    
    # Marcar el libro como no disponible
    libros_db[prestamo.id_libro]["disponible"] = False
    
    prestamos_db[prestamo_id_counter] = nuevo_prestamo
    prestamo_id_counter += 1
    
    return nuevo_prestamo


@app.post("/prestamos/{prestamo_id}/devolver", response_model=PrestamoResponse, tags=["Préstamos"])
def devolver_libro(prestamo_id: int, devolucion: Optional[Devolucion] = None):
    """
    Registrar la devolución de un libro prestado.
    
    Parámetros:
    - prestamo_id: ID del préstamo a completar
    - devolucion: objeto con fecha_devolucion (opcional, usa fecha actual si no se proporciona)
    """
    if prestamo_id not in prestamos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con ID {prestamo_id} no encontrado"
        )
    
    prestamo = prestamos_db[prestamo_id]
    
    # Validar que el préstamo esté vigente
    if prestamo["estado"] != "vigente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este préstamo ya ha sido completado o devuelto"
        )
    
    # Actualizar el préstamo
    fecha_devolucion = devolucion.fecha_devolucion if devolucion and devolucion.fecha_devolucion else datetime.now()
    prestamo["fecha_devolución_real"] = fecha_devolucion
    prestamo["estado"] = "completado"
    
    # Marcar el libro como disponible
    libros_db[prestamo["id_libro"]]["disponible"] = True
    
    return prestamo


# ==================== ENDPOINT DE SALUD ====================

@app.get("/health", tags=["Salud"])
def health_check():
    """Verificar que la API está en funcionamiento"""
    return {
        "status": "ok",
        "mensaje": "API Biblioteca funcionando correctamente",
        "timestamp": datetime.now()
    }


# ==================== INFORMACIÓN ====================

@app.get("/", tags=["Información"])
def root():
    """Información sobre la API"""
    return {
        "nombre": "API Biblioteca Universitaria",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
