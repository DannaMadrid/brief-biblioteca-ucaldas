# Prompt #7 - Resolución de Ejercicios Pendientes del Taller de Análisis V1 vs V2

**Fecha y hora:** 2026-05-19 00:00

**Propósito en una línea:** Completar los ejercicios pendientes del taller de análisis estructural v1/v2, con énfasis en la escritura del test unitario real del Ejercicio 4.1.

**Etapa del taller:** 3 (Bloque 3 – Bloque 4)

**IA usada:** Claude (Cowork)

---

## Prompt enviado (literal)

```
Actúa como un Ingeniero de Software Senior y Experto en Testing con Python.

---

## Contexto del Proyecto

Estás trabajando en un proyecto de análisis comparativo de dos versiones de una API REST de biblioteca universitaria.

Archivos de referencia obligatorios — léelos antes de escribir cualquier código:

1. Enunciado completo del taller:
   01-contexto/taller-analisis-v1-v2.md

2. Bitácora de avance (contiene las respuestas ya completadas y la descripción del estado actual):
   02-tu-trabajo/bitacora-taller-analisis.md

3. Implementación v2 (arquitectura Clean, 4 capas):
   biblioteca-api/app/services/prestamo_service.py
   biblioteca-api/app/repositories/prestamo_repo.py
   biblioteca-api/app/models/prestamo.py
   biblioteca-api/app/models/estudiante.py
   biblioteca-api/app/core/exceptions.py

4. Suite de tests de integración existente (para entender el patrón de fixtures):
   biblioteca-api/tests/conftest.py
   biblioteca-api/tests/test_prestamos.py

---

## Stack Técnico

- Lenguaje: Python 3.11+
- Framework: FastAPI
- Testing: pytest + unittest.mock (MagicMock)
- Persistencia: Memoria (sin base de datos real)

---

## Tarea Principal — Ejercicio 4.1 (Bloque 4)

El enunciado del taller pide escribir el siguiente test unitario en v2:

> "Escribe un test unitario para `CrearPrestamo` que verifique que un estudiante de
> posgrado puede tener hasta 5 préstamos simultáneos pero falla al intentar el sexto."

**Ruta de destino del archivo a crear:**
biblioteca-api/tests/unit/test_rn1_posgrado_unitario.py

**Reglas de implementación:**

1. UNITARIO PURO — No uses `TestClient` ni pases por HTTP. Instancia `PrestamoService`
   directamente con repositorios mockeados usando `MagicMock`.

2. AISLAMIENTO — El mock de `prestamo_repo.get_activos_by_estudiante()` debe devolver
   una lista de 5 objetos `Prestamo` para simular el límite ya alcanzado.

3. VERIFICACIÓN DE EXCEPCIÓN — El test debe confirmar que al intentar el sexto préstamo
   se lanza la excepción de dominio correcta (busca su nombre exacto en
   `biblioteca-api/app/core/exceptions.py`).

4. CASO COMPLEMENTARIO — Además del test del sexto fallo, agrega un segundo test que
   verifique que el quinto préstamo SÍ se permite (happy path del límite).

5. REFLEXIÓN — Al final del archivo, en un comentario de bloque, explica brevemente
   por qué este test sería más lento o imposible de escribir en v1.

**Crea también el archivo `biblioteca-api/tests/unit/__init__.py`** si no existe,
para que pytest descubra el subdirectorio.

---

## Tarea Secundaria — Verificación del Ejercicio 3.1 (Bloque 3)

El enunciado del taller pide ejecutar la suite y medir el tiempo. Una vez escritos
los tests del Ejercicio 4.1, ejecuta:

   pytest biblioteca-api/tests/ -v --tb=short

Registra en la bitácora:
- El número total de tests que pasan.
- El tiempo total de ejecución reportado por pytest.
- Confirma que los dos nuevos tests del Ejercicio 4.1 están en verde.

---

## Reglas de Ejecución

Fidelidad al código existente:
No modifiques ningún archivo fuera de `tests/unit/`. Si necesitas ajustar algo en
`prestamo_service.py` para que el test funcione, documenta el motivo antes de hacerlo.

Gestión de incertidumbre:
Si los nombres de clases, métodos o excepciones en el código real difieren de los
que menciona el enunciado (que usa TypeScript como referencia), adapta el test al
stack Python real que encuentres en los archivos.

Formato de salida esperado:
1. Contenido completo de `biblioteca-api/tests/unit/test_rn1_posgrado_unitario.py`
2. Resultado del comando pytest (salida literal o resumen fiel)
3. Actualización de la sección "Ejercicio 4.1" en `02-tu-trabajo/bitacora-taller-analisis.md`
   con el código del test y el resultado de ejecución
```

---

## Resumen de la respuesta de la IA

> [Completa después de ejecutar el prompt. Indica: archivos creados o modificados, número de tests nuevos, resultado de pytest, y cualquier decisión autónoma que haya tomado la IA —como renombrar una excepción o ajustar un import.]

---

## Mi evaluación

**¿La respuesta cumplió con lo que pedí?**

- [ ] Completamente.
- [ ] Parcialmente. Faltó: [...]
- [ ] No, se desvió. Hizo: [...]

**¿La acepté tal cual o la modifiqué?**

- [ ] Tal cual.
- [ ] La modifiqué a mano. Cambios: [...]
- [ ] Le pedí corrección con un prompt nuevo (ver prompt #8).
- [ ] La rechacé completamente. Razón: [...]

**¿Qué aprendí de esta interacción?**

> [Completa después de revisar el test generado y el resultado de pytest.]

---

## Notas para el siguiente prompt

- Si el test del sexto préstamo falla por un problema de nombres de modelo, revisar
  `biblioteca-api/app/models/estudiante.py` y ajustar los campos en el mock.
- La carpeta `tests/unit/` es nueva; asegurarse de que `pytest.ini` la incluya en
  el `testpaths` o que pytest la descubra automáticamente.
- Próximo paso posible: extender los tests unitarios a otras reglas de negocio (RN2,
  RN3, RN4) siguiendo el mismo patrón de MagicMock establecido en este ejercicio.
