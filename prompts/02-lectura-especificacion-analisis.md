# Prompt #2 - Lectura de Especificación y Análisis de Ambigüedades

**Fecha y hora:** 2026-05-12 11:00

**Propósito en una línea:** Inicializar proyecto FastAPI leyendo la especificación formal como fuente de verdad e identificar contradicciones antes de escribir código.

**Etapa del taller:** 2

**IA usada:** Claude Code

---

### Prompt enviado (literal)

```
Contexto y Rol:
Actúa como un Ingeniero de Software Senior experto en Python y FastAPI. Tu tarea es inicializar un proyecto siguiendo estrictamente un documento de requerimientos.

Instrucción Primaria:
Antes de generar cualquier código, lee y analiza detenidamente el archivo: 02-tu-trabajo\plantilla-especificacion.md. Este documento es la "fuente de la verdad".

Stack Técnico:

Lenguaje: Python 3.11+

Framework: FastAPI

Persistencia: Datos en memoria (usar diccionarios o listas de Python). No instales ni configures bases de datos (SQL/NoSQL).

Seguridad: Sin autenticación ni autorización en esta fase.

Interfaz: Solo API REST (sin frontend).

Testing: Pytest.

Reglas de Ejecución:

Fidelidad Extrema: No agregues funcionalidades, endpoints o lógica que no estén explícitamente mencionados en la especificación.

Estructura Limpia: Si el documento no define una estructura, utiliza una distribución estándar de FastAPI (ej. app/main.py, app/models/, app/routers/, tests/).

Gestión de Ambigüedad: Si encuentras alguna contradicción o falta de detalle en la especificación, detente y pregunta antes de asumir una solución.

Archivos Base: Genera primero README.md (con instrucciones de instalación), .gitignore (específico para Python), requirements.txt y .env (si aplica).

Flujo de Trabajo:

Fase 1 (Análisis): Confirma que has leído el archivo y presenta un árbol de estructura de carpetas propuesto.

Fase 2 (Aprobación): Espera mi validación del árbol antes de escribir el código de la lógica de negocio o los tests.
```

---

### Resumen de la respuesta de la IA

Leyó `02-tu-trabajo/plantilla-especificacion.md` completo. Detectó 5 contradicciones/ambigüedades críticas antes de escribir una sola línea de código: (C1) conflicto en el límite de préstamos de pregrado entre Sección 1 y RN1, (C2) campo `estado` faltante en Ejemplar, (C3) campos `estado` y `fecha_pago` faltantes en Multa, (C4) ambigüedad entre `cantidad` en Ejemplar vs. préstamos por copia individual, (C5) reglas de renovación no definidas. No generó ningún código; detuvo el flujo para recibir respuestas antes de continuar. Propuso el árbol de carpetas solo después de que se resolvieran las ambigüedades.

---

### Mi evaluación

**¿La respuesta cumplió con lo que pedí?**

- [x] Completamente.

**¿La acepté tal cual o la modifiqué?**

- [x] La Modifiqué.

**¿Qué aprendí de esta interacción?**

> La IA identificó contradicciones reales en mi especificación que yo había pasado por alto. El hecho de que se detuviera a preguntar en lugar de asumir demostró que el prompt de "Gestión de Ambigüedad" funcionó correctamente.

---

## Notas para el siguiente prompt

- Las 5 ambigüedades deben resolverse antes de que la IA genere cualquier árbol de carpetas.
- C1 y C5 son las más críticas para la lógica de negocio.
