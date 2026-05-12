# Guía de Prueba - API Biblioteca Universitaria

Esta guía contiene ejemplos de cómo probar todos los endpoints del API usando `curl`.

## Requisitos Previos

- Tener `curl` instalado (generalmente viene incluido en Windows 10+, Linux y macOS)
- El servidor debe estar corriendo: `python main.py`

## Inicio Rápido

### 1. Verificar que el servidor está corriendo
```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "mensaje": "API Biblioteca funcionando correctamente",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

---

## LIBROS

### 1.1 Listar todos los libros
```bash
curl http://localhost:8000/libros
```

### 1.2 Listar solo libros disponibles
```bash
curl "http://localhost:8000/libros?disponible=true"
```

### 1.3 Listar solo libros NO disponibles
```bash
curl "http://localhost:8000/libros?disponible=false"
```

### 1.4 Obtener detalles de un libro específico
```bash
curl http://localhost:8000/libros/1
```

### 1.5 Crear un nuevo libro
```bash
curl -X POST http://localhost:8000/libros \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Algoritmos en Python",
    "autor": "Thomas Cormen",
    "isbn": "ISBN-ALG-001"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 4,
  "titulo": "Algoritmos en Python",
  "autor": "Thomas Cormen",
  "isbn": "ISBN-ALG-001",
  "disponible": true
}
```

### 1.6 Intentar crear un libro con ISBN duplicado (error esperado)
```bash
curl -X POST http://localhost:8000/libros \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Otro Titulo",
    "autor": "Otro Autor",
    "isbn": "ISBN-001"
  }'
```

**Respuesta esperada (400):**
```json
{
  "detail": "Ya existe un libro con ISBN ISBN-001"
}
```

---

## PRÉSTAMOS

### 2.1 Listar todos los préstamos vigentes
```bash
curl http://localhost:8000/prestamos
```

### 2.2 Listar todos los préstamos completados
```bash
curl "http://localhost:8000/prestamos?estado=completado"
```

### 2.3 Obtener detalles de un préstamo específico
```bash
curl http://localhost:8000/prestamos/1
```

### 2.4 Crear un nuevo préstamo (14 días de plazo)

Para Windows (PowerShell):
```powershell
$fecha = (Get-Date).AddDays(14).ToString("yyyy-MM-ddTHH:mm:ss")
$body = @{
    id_libro = 1
    id_usuario = "estudiante_001"
    fecha_devolución_esperada = $fecha
} | ConvertTo-Json

curl -X POST http://localhost:8000/prestamos `
  -H "Content-Type: application/json" `
  -d $body
```

Para Linux/macOS/Git Bash:
```bash
FECHA=$(date -u -d "+14 days" +"%Y-%m-%dT%H:%M:%S")
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d "{
    \"id_libro\": 1,
    \"id_usuario\": \"estudiante_001\",
    \"fecha_devolución_esperada\": \"$FECHA\"
  }"
```

O simplemente con fecha hardcoded:
```bash
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d '{
    "id_libro": 1,
    "id_usuario": "estudiante_001",
    "fecha_devolución_esperada": "2024-02-15T23:59:59"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 1,
  "id_libro": 1,
  "id_usuario": "estudiante_001",
  "fecha_prestamo": "2024-01-15T10:30:00.123456",
  "fecha_devolución_esperada": "2024-02-15T23:59:59",
  "fecha_devolución_real": null,
  "estado": "vigente"
}
```

### 2.5 Intentar crear préstamo de libro no disponible (error esperado)

Primero, el libro 3 no está disponible. Intenta hacer un préstamo:
```bash
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d '{
    "id_libro": 3,
    "id_usuario": "estudiante_002",
    "fecha_devolución_esperada": "2024-02-15T23:59:59"
  }'
```

**Respuesta esperada (400):**
```json
{
  "detail": "El libro con ID 3 no está disponible"
}
```

### 2.6 Intentar crear préstamo con fecha de devolución en el pasado (error esperado)
```bash
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d '{
    "id_libro": 2,
    "id_usuario": "estudiante_003",
    "fecha_devolución_esperada": "2024-01-01T10:00:00"
  }'
```

**Respuesta esperada (400):**
```json
{
  "detail": "La fecha de devolución esperada debe ser en el futuro"
}
```

### 2.7 Intentar hacer préstamo de libro que no existe (error esperado)
```bash
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d '{
    "id_libro": 999,
    "id_usuario": "estudiante_004",
    "fecha_devolución_esperada": "2024-02-15T23:59:59"
  }'
```

**Respuesta esperada (404):**
```json
{
  "detail": "Libro con ID 999 no encontrado"
}
```

---

## DEVOLUCIONES

### 3.1 Devolver un libro (usando fecha actual)
```bash
curl -X POST http://localhost:8000/prestamos/1/devolver \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "id_libro": 1,
  "id_usuario": "estudiante_001",
  "fecha_prestamo": "2024-01-15T10:30:00.123456",
  "fecha_devolución_esperada": "2024-02-15T23:59:59",
  "fecha_devolución_real": "2024-01-20T15:45:30.987654",
  "estado": "completado"
}
```

### 3.2 Devolver un libro con fecha específica
```bash
curl -X POST http://localhost:8000/prestamos/2/devolver \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_devolucion": "2024-01-25T14:30:00"
  }'
```

### 3.3 Intentar devolver un préstamo ya completado (error esperado)
```bash
curl -X POST http://localhost:8000/prestamos/1/devolver \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Respuesta esperada (400):**
```json
{
  "detail": "Este préstamo ya ha sido completado o devuelto"
}
```

---

## Flujo Completo de Ejemplo

Este es un flujo completo típico:

### Paso 1: Verificar disponibilidad de libros
```bash
curl "http://localhost:8000/libros?disponible=true"
```

### Paso 2: Crear un préstamo
```bash
curl -X POST http://localhost:8000/prestamos \
  -H "Content-Type: application/json" \
  -d '{
    "id_libro": 2,
    "id_usuario": "estudiante_001",
    "fecha_devolución_esperada": "2024-02-10T23:59:59"
  }'
```

Nota: Guarda el ID del préstamo de la respuesta (ej: 2)

### Paso 3: Consultar el libro ahora debe estar no disponible
```bash
curl http://localhost:8000/libros/2
```

### Paso 4: Listar préstamos vigentes
```bash
curl http://localhost:8000/prestamos?estado=vigente
```

### Paso 5: Consultar detalles del préstamo
```bash
curl http://localhost:8000/prestamos/2
```

### Paso 6: Devolver el libro
```bash
curl -X POST http://localhost:8000/prestamos/2/devolver \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Paso 7: Verificar que el libro está disponible de nuevo
```bash
curl http://localhost:8000/libros/2
```

### Paso 8: Verificar que el préstamo está completado
```bash
curl http://localhost:8000/prestamos?estado=completado
```

---

## Usando Python para pruebas

Si prefieres usar Python, ejecuta:
```bash
pip install requests
python ejemplo_uso.py
```

---

## Documentación Interactiva

El API cuenta con documentación interactiva donde puedes probar todos los endpoints:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

¡Puedes probar todos los endpoints directamente desde el navegador!

---

## Notas Importantes

1. **Datos en Memoria**: Los datos se pierden cuando reinicia el servidor
2. **IDs Automáticos**: Se asignan automáticamente en orden secuencial
3. **Validación**: El API valida todos los datos antes de procesar
4. **Estados HTTP**: 
   - `200`: OK
   - `201`: Creado
   - `400`: Solicitud inválida
   - `404`: No encontrado
   - `500`: Error del servidor

---

## Solución de Problemas

### "Conexión rechazada"
- Asegúrate de que el servidor está corriendo: `python main.py`
- Verifica que estés usando el puerto correcto: `8000`

### "ISBN duplicado"
- Cada libro debe tener un ISBN único
- Verifica que el ISBN no exista ya en el sistema

### "Libro no disponible"
- El libro ya tiene un préstamo vigente
- Espera a que se devuelva o crea un préstamo de otro libro

### "Fecha de devolución en el pasado"
- La fecha de devolución debe ser posterior a la fecha actual
- Usa una fecha futura: mínimo mañana
