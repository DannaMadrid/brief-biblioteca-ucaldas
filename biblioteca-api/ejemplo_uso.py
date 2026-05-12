"""
Script de ejemplo para probar el API de Biblioteca Universitaria
Asegúrate de que el servidor esté corriendo en http://localhost:8000
"""

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Configurar colores para la salida
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")


# ==================== LIBROS ====================

def ejemplo_listar_libros():
    print_header("1. Listar todos los libros")
    
    response = requests.get(f"{BASE_URL}/libros")
    print_info(f"Status Code: {response.status_code}")
    
    libros = response.json()
    print_success(f"Se encontraron {len(libros)} libros:")
    for libro in libros:
        disponible = "✓ Disponible" if libro["disponible"] else "✗ No disponible"
        print(f"  - [{libro['id']}] {libro['titulo']} - {libro['autor']} ({disponible})")


def ejemplo_listar_libros_disponibles():
    print_header("2. Listar libros disponibles")
    
    response = requests.get(f"{BASE_URL}/libros?disponible=true")
    print_info(f"Status Code: {response.status_code}")
    
    libros = response.json()
    print_success(f"Se encontraron {len(libros)} libros disponibles:")
    for libro in libros:
        print(f"  - [{libro['id']}] {libro['titulo']}")


def ejemplo_obtener_libro():
    print_header("3. Obtener detalles de un libro específico")
    
    libro_id = 1
    response = requests.get(f"{BASE_URL}/libros/{libro_id}")
    print_info(f"Status Code: {response.status_code}")
    
    libro = response.json()
    print_success(f"Libro encontrado:")
    print(f"  ID: {libro['id']}")
    print(f"  Título: {libro['titulo']}")
    print(f"  Autor: {libro['autor']}")
    print(f"  ISBN: {libro['isbn']}")
    print(f"  Disponible: {'Sí' if libro['disponible'] else 'No'}")


def ejemplo_crear_libro():
    print_header("4. Crear un nuevo libro")
    
    nuevo_libro = {
        "titulo": "Introducción a FastAPI",
        "autor": "Sebastián Ramírez",
        "isbn": "ISBN-FASTAPI-001"
    }
    
    response = requests.post(f"{BASE_URL}/libros", json=nuevo_libro)
    print_info(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        libro_creado = response.json()
        print_success(f"Libro creado exitosamente:")
        print(f"  ID: {libro_creado['id']}")
        print(f"  Título: {libro_creado['titulo']}")
        print(f"  Autor: {libro_creado['autor']}")
        return libro_creado['id']
    else:
        print_error(f"Error al crear libro: {response.json()}")
        return None


# ==================== PRÉSTAMOS ====================

def ejemplo_crear_prestamo():
    print_header("5. Crear un préstamo")
    
    fecha_devolucion = datetime.now() + timedelta(days=14)
    
    nuevo_prestamo = {
        "id_libro": 1,
        "id_usuario": "estudiante_001",
        "fecha_devolución_esperada": fecha_devolucion.isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/prestamos", json=nuevo_prestamo)
    print_info(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        prestamo_creado = response.json()
        print_success(f"Préstamo creado exitosamente:")
        print(f"  ID Préstamo: {prestamo_creado['id']}")
        print(f"  ID Libro: {prestamo_creado['id_libro']}")
        print(f"  Usuario: {prestamo_creado['id_usuario']}")
        print(f"  Fecha de Préstamo: {prestamo_creado['fecha_prestamo']}")
        print(f"  Fecha de Devolución Esperada: {prestamo_creado['fecha_devolución_esperada']}")
        print(f"  Estado: {prestamo_creado['estado']}")
        return prestamo_creado['id']
    else:
        print_error(f"Error al crear préstamo: {response.json()}")
        return None


def ejemplo_listar_prestamos_vigentes():
    print_header("6. Listar préstamos vigentes")
    
    response = requests.get(f"{BASE_URL}/prestamos")
    print_info(f"Status Code: {response.status_code}")
    
    prestamos = response.json()
    print_success(f"Se encontraron {len(prestamos)} préstamos vigentes:")
    for prestamo in prestamos:
        print(f"  - [ID: {prestamo['id']}] Libro {prestamo['id_libro']} - "
              f"Usuario: {prestamo['id_usuario']} - "
              f"Estado: {prestamo['estado']}")


def ejemplo_obtener_prestamo():
    print_header("7. Obtener detalles de un préstamo")
    
    prestamo_id = 1
    response = requests.get(f"{BASE_URL}/prestamos/{prestamo_id}")
    print_info(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        prestamo = response.json()
        print_success(f"Préstamo encontrado:")
        print(f"  ID: {prestamo['id']}")
        print(f"  ID Libro: {prestamo['id_libro']}")
        print(f"  Usuario: {prestamo['id_usuario']}")
        print(f"  Fecha de Préstamo: {prestamo['fecha_prestamo']}")
        print(f"  Fecha de Devolución Esperada: {prestamo['fecha_devolución_esperada']}")
        print(f"  Fecha de Devolución Real: {prestamo['fecha_devolución_real']}")
        print(f"  Estado: {prestamo['estado']}")
    else:
        print_error(f"Préstamo no encontrado")


def ejemplo_devolver_libro(prestamo_id):
    print_header("8. Devolver un libro")
    
    print_info(f"Devolviendo préstamo ID: {prestamo_id}")
    
    response = requests.post(
        f"{BASE_URL}/prestamos/{prestamo_id}/devolver",
        json={}
    )
    print_info(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        prestamo_actualizado = response.json()
        print_success(f"Libro devuelto exitosamente:")
        print(f"  ID Préstamo: {prestamo_actualizado['id']}")
        print(f"  Estado: {prestamo_actualizado['estado']}")
        print(f"  Fecha de Devolución Real: {prestamo_actualizado['fecha_devolución_real']}")
    else:
        print_error(f"Error al devolver libro: {response.json()}")


def ejemplo_health_check():
    print_header("9. Verificar estado del API")
    
    response = requests.get(f"{BASE_URL}/health")
    print_info(f"Status Code: {response.status_code}")
    
    health = response.json()
    print_success(f"API Status: {health['status']}")
    print(f"  Mensaje: {health['mensaje']}")
    print(f"  Timestamp: {health['timestamp']}")


# ==================== MAIN ====================

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     EJEMPLOS DE USO - API BIBLIOTECA UNIVERSITARIA       ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    try:
        # Verificar conexión
        print_info("Verificando conexión con el servidor...")
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            print_success("¡Conexión establecida!")
        else:
            print_error("No se pudo conectar al servidor")
            print_error("Asegúrate de que el servidor está corriendo en http://localhost:8000")
            return
        
        # Ejemplos de Libros
        ejemplo_listar_libros()
        ejemplo_listar_libros_disponibles()
        ejemplo_obtener_libro()
        nuevo_libro_id = ejemplo_crear_libro()
        
        # Ejemplos de Préstamos
        prestamo_id = ejemplo_crear_prestamo()
        ejemplo_listar_prestamos_vigentes()
        ejemplo_obtener_prestamo()
        
        if prestamo_id:
            ejemplo_devolver_libro(prestamo_id)
            ejemplo_listar_prestamos_vigentes()
        
        # Health Check
        ejemplo_health_check()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ¡Todos los ejemplos completados!{Colors.END}\n")
        
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_error("Por favor, asegúrate de que el servidor está corriendo:")
        print_error("  python main.py")
    except Exception as e:
        print_error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
