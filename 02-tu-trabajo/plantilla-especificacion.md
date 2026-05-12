# Especificación Formal — Sistema de Préstamo de Libros

> **Autor:** Danna Alexandra Madrid Roa
> **Fecha:** 5-Mayo-2025
> **Versión:** 1.0
> **Brief de origen:** Correo de Diana Restrepo, Coordinadora de Biblioteca

> Lo que está entre corchetes `[...]` es lo que tú debes escribir.

---

## 1. Propósito del sistema

El sistema consulta que libros estan disponibles para prestamos, consulta catalogo de libros, consultar el historial de prestamos por estudiantes registrar prestamos de estudiantes, pregrado pueden prestar max 3 al tiempo y si son de postgrado max 5, registrar devoluciones y aviso de prestamos vencidos y que el sistema valide segun tipo de libro la duración del prestamo, donde si esta marcado como de alta demanda solo puede prestarse 3 días, de lo contrario se prestan 15 días y además calcular las multas por retraso de cada libro

---

## 2. Alcance

**Incluido en esta versión:**

- Consultar catálogo de libros
- Consultar libros disponibles para prestamo
- Solicitar un prestamo
- Registrar devolución de prestamos de libros
- Aviso de prestamos vencidos 
- Validar el número maximo de libros prestados por estudiante
- Validar duración del prestamo segun tipo de libro, si estan marcado de alta demanda 3 días de prestamo y de lo contrario 15 días de préstamo
- Validar renovación de prestamos según el tipo de libro
- Gestionar multas por devolución tardía, la bilioteca cobra 2000 por día de retraso por cada libro
- Calcular la multa coparando la fecha de devolución con la fecha en que debia haberlo devuelto
- Validar que mientras el estudiante tenga multas pendiente sin pagar, tampoco puede prestar libros


**Explícitamente fuera del alcance:**

- [Lista lo que el correo menciona pero NO se va a implementar. Por ejemplo: el caso de los profesores investigadores.]
- Catalogar libros
- Autenticación
- Implementar frontend, app móvil o portal web
- Implementar base de datos

---

## 3. Modelo de datos

### Entidad: Libro

| Campo  | Tipo | Obligatorio | Descripción   |
| Codigo | str  | sí          | Código unico de inventario |
| Titulo | str  | sí          | Titulo del libro |
| Autor  | str  | sí          | Autor del libro |
| Sala   | str  | sí          | Sala donde esta ubicado el libro |
| alta_demanda | bool | sí | Indica si el libro pertenece a sala de reserva o alta demanda |

### Entidad: Ejemplar

| Campo     | Tipo | Obligatorio | Descripción   |
| id        | str  | sí          | Identificador ejemplar |
| Cod_Libro  | str  | sí          | codigo del libro referenciado |
| Cantidad  | int  | sí          | cantidad de ejemplares del libro|

### Entidad: Estudiante

| Campo              | Tipo | Obligatorio | Descripción   |
| codigo             | str  | sí          | código único de estudiante |
| nombre             | str  | sí          | Nombre de estudiante |
| programa_academico | str  | sí          | código único de estudiante |
| nivel_academico    | str  | sí          | Decir si es de pregrado o postgrado |

### Entidad: Préstamo

[Tabla de campos. Aquí va estudiante_id, ejemplar_id, fecha_prestamo, fecha_devolucion_esperada, fecha_devolucion_real, estado, etc.]
| Campo                    | Tipo | Obligatorio | Descripción   |
| Id                       | str  | sí          | Id prestamo |
| estudiante_cod           | str  | sí          | Codigo de estudiante |
| ejemplar_id              | str  | sí          | código de ejemplar |
| fecha_prestammo          | date | sí          |  fecha de cuando se realizo el prestamo |
| fecha_devolucion_esperada | date | sí         | fecha esperada de decoluación |
| estado                    | str | sí          | estado del prestamo |

### Entidad: Multa

| Campo                    | Tipo | Obligatorio | Descripción   |
| Id                       | str  | sí          | Id multa |
| estudiante_cod           | str  | sí          | Codigo de estudiante |
| ejemplar_id              | str  | sí          | código de ejemplar |
| prestamo_id              | str  | sí          |  id del prestamo |
| fecha_devolucion_real    | date | sí          | fecha esperada de decoluación |
| dias_retraso             | int  | sí          | cantidad de dias de retaso |
| valor_total              | float | sí         | Total de la multa |

### Entidad: SolicitudReserva

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| id | str | sí | Identificador único de la solicitud. |
| estudiante_codigo | str | sí | Código del estudiante que espera el libro. |
| libro_codigo | str | sí | Código del libro solicitado. |
| fecha_solicitud | date | sí | Fecha en la que se registró la solicitud. |
| estado | str | sí | Estado de la solicitud: `activa`, `cancelada`, `atendida`. |

### Diagrama de relaciones

```
[Dibuja con texto las relaciones. Por ejemplo:

Libro 1 --- N Ejemplar
Estudiante 1 --- N Prestamo
Ejemplar 1 --- N Prestamo (a lo largo del tiempo)
Prestamo 0..1 --- 1 Multa

Estudiante 1 --- N Multa
Un estudiante puede acumular varias multas.

Libro 1 --- N SolicitudReserva

Estudiante 1 --- N SolicitudReserva
]
```

---

## 4. Endpoints REST

| Método | Ruta | Propósito | Body / Query | Respuesta éxito | Códigos error posibles |
|---|---|---|---|---|---|
| `GET` | `/libros` | Listar el catálogo de libros | Query opcional: `titulo`, `autor`, `disponible`, `alta_demanda` | `200` con lista de libros | `500` |
| `GET` | `/libros/{codigo}` | Consultar el detalle de un libro | Path param: `codigo` | `200` con detalle del libro y sus ejemplares | `404`, `500` |
| `GET` | `/ejemplares/disponibles` | Consultar ejemplares disponibles para préstamo | Query opcional: `libro_codigo` | `200` con lista de ejemplares disponibles | `404`, `500` |
| `POST` | `/prestamos` | Registrar un nuevo préstamo | `{ "estudiante_codigo": "string", "ejemplar_id": "string" }` | `201` con préstamo creado | `400`, `404`, `409`, `500` |
| `POST` | `/prestamos/{id}/devolucion` | Registrar la devolución de un préstamo | `{ "fecha_devolucion_real": "YYYY-MM-DD" }` | `200` con préstamo actualizado y multa si aplica | `400`, `404`, `409`, `500` |
| `POST` | `/prestamos/{id}/renovacion` | Renovar un préstamo activo | `{ "fecha_renovacion": "YYYY-MM-DD" }` | `200` con préstamo renovado | `400`, `404`, `409`, `500` |
| `GET` | `/prestamos/vigentes` | Consultar préstamos activos o vigentes | Query opcional: `estudiante_codigo` | `200` con lista de préstamos vigentes | `404`, `500` |
| `GET` | `/prestamos/vencidos` | Consultar préstamos vencidos | Query opcional: `fecha_actual` | `200` con lista de préstamos vencidos | `500` |
| `GET` | `/estudiantes/{codigo}/historial` | Consultar historial de préstamos de un estudiante | Path param: `codigo` | `200` con historial de préstamos | `404`, `500` |
| `GET` | `/estudiantes/{codigo}/multas` | Consultar multas de un estudiante | Path param: `codigo` | `200` con lista de multas | `404`, `500` |
| `POST` | `/multas/{id}/pago` | Registrar el pago de una multa | `{ "fecha_pago": "YYYY-MM-DD" }` | `200` con multa marcada como pagada | `400`, `404`, `500` |
| `POST` | `/reservas` | Registrar solicitud de espera por un libro | `{ "estudiante_codigo": "string", "libro_codigo": "string" }` | `201` con reserva creada | `400`, `404`, `409`, `500` |


---

## 5. Reglas de negocio

### RN1 — [nombre corto de la regla]

- **Trigger:** [cuándo se evalúa]
- **Condición:** [qué se valida exactamente, en términos precisos]
- **Acción si cumple:** [qué hace el sistema]
- **Acción si no cumple:** [código HTTP, mensaje, qué retorna]

**Ejemplo:**

### RN1 — Límite de préstamos por tipo de estudiante

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:**
  - Estudiante de pregrado: máximo 3 préstamos con `estado = "activo"`.
  - Estudiante de posgrado: máximo 5 préstamos con `estado = "activo"`.
- **Acción si cumple:** continuar con el flujo de creación.
- **Acción si no cumple:** retornar `409 Conflict` con `{error: "limite_prestamos_alcanzado", limite: N, actuales: M}`.

[Llena RN2, RN3, RN4... hasta cubrir todas las reglas del correo.]

### RN2 — Bloqueo por préstamo vencido

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:** el estudiante no debe tener préstamos activos cuya `fecha_devolucion_esperada` sea menor a la fecha actual.
- **Acción si cumple:** continuar con el flujo de creación del préstamo.
- **Acción si no cumple:** retornar `409 Conflict` con:

```json
{
  "error": "prestamo_vencido_pendiente",
  "mensaje": "El estudiante tiene préstamos vencidos sin devolver."
}
```

### RN3 — Bloqueo por multas pendientes

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:** el estudiante no debe tener multas con `estado = "pendiente"`.
- **Acción si cumple:** continuar con el flujo de creación del préstamo.
- **Acción si no cumple:** retornar `409 Conflict` con:

```json
{
  "error": "multa_pendiente",
  "mensaje": "El estudiante tiene multas pendientes de pago."
}
```

### RN4 — Disponibilidad del ejemplar

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:** el ejemplar solicitado debe tener `estado = "disponible"`.
- **Acción si cumple:** crear el préstamo y cambiar el estado del ejemplar a `prestado`.
- **Acción si no cumple:** retornar `409 Conflict` con:

```json
{
  "error": "ejemplar_no_disponible",
  "mensaje": "El ejemplar no está disponible para préstamo."
}
```

### RN5 — Duración del préstamo según tipo de libro

- **Trigger:** al crear un préstamo o renovar un préstamo.
- **Condición:**
  - Si el libro tiene `alta_demanda = true`, el plazo será de 3 días.
  - Si el libro tiene `alta_demanda = false`, el plazo será de 15 días.
- **Acción si cumple:** calcular `fecha_devolucion_esperada` sumando los días correspondientes.
- **Acción si no cumple:** no aplica, porque el cálculo lo realiza automáticamente el sistema.


### RN6 — Devolución de préstamo

- **Trigger:** al recibir `POST /prestamos/{id}/devolucion`.
- **Condición:** el préstamo debe existir y tener `estado = "activo"` o `estado = "vencido"`.
- **Acción si cumple:**
  - Registrar `fecha_devolucion_real`.
  - Cambiar el estado del préstamo a `devuelto`.
  - Cambiar el estado del ejemplar a `disponible`.
  - Calcular multa si hay retraso.
- **Acción si no cumple:** retornar `409 Conflict` con:

```json
{
  "error": "prestamo_no_devolvible",
  "mensaje": "El préstamo no puede ser devuelto porque ya fue cerrado o no está activo."
}
```

### RN7 — Cálculo de multa por devolución tardía

- **Trigger:** al registrar una devolución.
- **Condición:** `fecha_devolucion_real` es mayor que `fecha_devolucion_esperada`.
- **Acción si cumple:**
  - Calcular días de retraso.
  - Multiplicar los días de retraso por `2000`.
  - Crear una multa con estado `pendiente`.
  - Asociar la multa al estudiante y al préstamo.
- **Acción si no cumple:**
---

## 6. Decisiones tomadas (lo que el correo no dice)

### D1 — [Decisión que tomaste]

- **Contexto:** [qué hueco había]
- **Decisión:** [qué decidiste]
- **Justificación:** [por qué esta decisión y no otra]

**Ejemplo:**

### D1 — Cálculo de días para multa

- **Contexto:** el correo no precisa si los días de retraso son calendario o hábiles.
- **Decisión:** usar días calendario.
- **Justificación:** es la interpretación más simple y se alinea con lo que la mayoría de bibliotecas hacen.

[Mínimo 5 decisiones documentadas.]

### D2, D3, D4, D5...

---

## 7. Códigos HTTP usados

| Código | Significado | Cuándo se usa |
|---|---|---|
| 200 | OK | GET exitosos |
| 201 | Created | POST exitosos que crean recursos |
| 400 | Bad Request | Body malformado o validación fallida |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Reglas de negocio violadas (límite alcanzado, duplicado, etc.) |
| 500 | Internal Server Error | Error no controlado del servidor |

[Si usas otros, agrégalos.]

---

## 8. Restricciones técnicas

- **Stack:** [Python + FastAPI]
- **Persistencia:** datos en memoria. No usar base de datos.
- **Sin autenticación** en esta versión.
- **Sin frontend** en esta versión. Solo API REST.