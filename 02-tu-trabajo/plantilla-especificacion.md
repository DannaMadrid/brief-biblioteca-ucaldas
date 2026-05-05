# Especificación Formal — Sistema de Préstamo de Libros

> **Autor:** Danna Alexandra Madrid Roa
> **Fecha:** 5-Mayo-2025
> **Versión:** 1.0
> **Brief de origen:** Correo de Diana Restrepo, Coordinadora de Biblioteca

> Lo que está entre corchetes `[...]` es lo que tú debes escribir.

---

## 1. Propósito del sistema

El sistema consulta que libros estan disponibles para prestamos, consulta catalogo de libros, consultar el historial de prestamos por estudiantes registrar prestamos de estudiantes, pregrado pueden prestar max 5 al tiempo y si son de postgrado max 5, registrar devoluciones y aviso de prestamos vencidos y que el sistema valide segun tipo de libro la duración del prestamo, donde si esta marcado como de alta demanda solo puede prestarse 3 días, de lo contrario se prestan 15 días y además calcular las multas por retraso de cada libro

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

---

## 3. Modelo de datos

### Entidad: Libro

| Campo  | Tipo | Obligatorio | Descripción   |
| Codigo | str  | sí          | Código unico de inventario |
| Titulo | str  | sí          | Titulo del libro |
| Autor  | str  | sí          | Autor del libro |
| Sala   | str  | sí          | Sala donde esta ubicado el libro |

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

### Diagrama de relaciones

```
[Dibuja con texto las relaciones. Por ejemplo:

Libro 1 --- N Ejemplar
Estudiante 1 --- N Prestamo
Ejemplar 1 --- N Prestamo (a lo largo del tiempo)
Prestamo 0..1 --- 1 Multa
]
```

---

## 4. Endpoints REST

| Método | Ruta | Propósito | Body / Query | Respuesta éxito | Códigos error posibles |
|---|---|---|---|---|---|
| `GET` | `/libros` | Listar catálogo | filtros opcionales | `200` con lista | - |
| `GET` | `/libros/:id` | Detalle libro | - | `200` con objeto | `404` |
| `POST` | `/prestamos` | Crear préstamo | `{estudiante_id, ejemplar_id}` | `201` con préstamo | `400`, `404`, `409` |
| ... | ... | ... | ... | ... | ... |

[Llena la tabla con todos los endpoints que necesitas. Mínimo 8.]

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

### RN2 — [...]

[...]

### RN3 — [...]

[...]


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