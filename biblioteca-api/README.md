# API Biblioteca Universitaria

API REST en Python para gestionar préstamos y devoluciones de libros en una biblioteca universitaria.

## Características

- ✅ Gestión de libros (listar, crear, obtener detalles)
- ✅ Gestión de préstamos (crear, listar, consultar vigentes)
- ✅ Devolución de libros
- ✅ Control de disponibilidad de libros
- ✅ Datos en memoria
- ✅ Documentación automática con Swagger UI

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Navega a la carpeta del proyecto:
```bash
cd biblioteca-api
```

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Inicia el servidor:
```bash
python main.py
```

El API estará disponible en: `http://localhost:8000`

### Acceso a la documentación interactiva:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Libros

#### Listar todos los libros
```
GET /libros
```
Parámetro opcional: `disponible` (true/false)

**Ejemplo:**
```bash
curl http://localhost:8000/libros
curl http://localhost:8000/libros?disponible=true
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "titulo": "Python 101",
    "autor": "Guido van Rossum",
    "isbn": "ISBN-001",
    "disponible": true
  },
  {
    "id": 2,
    "titulo": "Clean Code",
    "autor": "Robert C. Martin",
    "isbn": "ISBN-002",
    "disponible": true
  }
]
```

#### Obtener detalles de un libro
```
GET /libros/{libro_id}
```

**Ejemplo:**
```bash
curl http://localhost:8000/libros/1
```

#### Crear un nuevo libro
```
POST /libros
Content-Type: application/json
```

**Cuerpo de la solicitud:**
```json
{
  "titulo": "Nuevo Libro",
  "autor": "Autor del Libro",
  "isbn": "ISBN-123",
  "disponible": true
}
```

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/libros \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Learning FastAPI",
    "autor": "Sebastián Ramírez",
    "isbn": "ISBN-456"
  }'
```

---

### Préstamos

#### Listar préstamos vigentes
```
GET /prestamos
```
Parámetro opcional: `estado` (vigente/completado, por defecto vigente)

**Ejemplo:**
```bash
curl http://localhost:8000/prestamos
curl http://localhost:8000/prestamos?estado=vigente
curl http://localhost:8000/prestamos?estado=completado
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "id_libro": 1,
    "id_usuario": "usuario123",
    "fecha_prestamo": "2024-01-15T10:30:00",
    "fecha_devolución_esperada": "2024-02-15T00:00:00",
    "fecha_devolución_real": null,
    "estado": "vigente"
  }
]
```

#### Obtener detalles de un préstamo
```
GET /prestamos/{prestamo_id}
```

**Ejemplo:**
```bash
curl http://localhost:8000/prestamos/1
```

#### Crear un nuevo préstamo
```
POST /prestamos
Content-Type: application/json
```

**Cuerpo de la solicitud:**
```json
{
  "id_libro": 1,
  "id_usuario": "usuario123",
  "fecha_devolución_esperada": "2024-02-15T23:59:59"
}
```

**Validaciones:**
- El libro debe existir
- El libro debe estar disponible
- La fecha de devolución debe ser en el futuro

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d '{
    "id_libro": 1,
    "id_usuario": "estudiante_001",
    "fecha_devolución_esperada": "2024-02-20T23:59:59"
  }'
```

#### Devolver un libro
```
POST /prestamos/{prestamo_id}/devolver
Content-Type: application/json
```

**Cuerpo de la solicitud (opcional):**
```json
{
  "fecha_devolucion": "2024-01-20T15:30:00"
}
Si no se proporciona, se usa la fecha actual.
```

**Ejemplo:**
```bash
curl -X POST http://localhost:8000/prestamos/1/devolver \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_devolucion": "2024-01-20T15:30:00"
  }'

# O sin fecha (usa fecha actual)
curl -X POST http://localhost:8000/prestamos/1/devolver \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### Salud

#### Verificar estado del API
```
GET /health
```

**Ejemplo:**
```bash
curl http://localhost:8000/health
```

## Estructura de Datos

### Libro
```json
{
  "id": number,
  "titulo": string,
  "autor": string,
  "isbn": string,
  "disponible": boolean
}
```

### Préstamo
```json
{
  "id": number,
  "id_libro": number,
  "id_usuario": string,
  "fecha_prestamo": datetime,
  "fecha_devolución_esperada": datetime,
  "fecha_devolución_real": datetime | null,
  "estado": "vigente" | "completado"
}
```

## Datos Iniciales

El API viene con 3 libros precargados:

1. **Python 101** - Guido van Rossum (ISBN-001) - Disponible
2. **Clean Code** - Robert C. Martin (ISBN-002) - Disponible
3. **Design Patterns** - Gang of Four (ISBN-003) - No disponible

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Solicitud inválida
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

## Notas Importantes

- ⚠️ Los datos se almacenan en memoria, se perderán al reiniciar el servidor
- ⚠️ Para producción, considera usar una base de datos persistente
- ⚠️ Los IDs se generan automáticamente en orden secuencial

## Mejoras Futuras

- [ ] Persistencia con base de datos (SQLite, PostgreSQL)
- [ ] Autenticación y autorización
- [ ] Renovación de préstamos
- [ ] Multas por devolución tardía
- [ ] Notificaciones de devolución próxima
- [ ] Búsqueda avanzada de libros
- [ ] Historial de préstamos por usuario
- [ ] Control de inventario

## Licencia

Proyecto educativo - Biblioteca Universitaria UCaldas
