# Prompt #3 - Resolución de Ambigüedades y Propuesta de Árbol

**Fecha y hora:** 2026-05-12 11:20

**Propósito en una línea:** Responder las 5 ambigüedades detectadas por la IA y permitir que proponga el árbol de carpetas.

**Etapa del taller:** 2

**IA usada:** Claude Code

---

### Prompt enviado (literal)

```
c1: El limite para pregrado es 3 y para postgrado es 5
c2: Si
c3: Agregarlo
c4: Para explicar lo que quiero es "Si el libro tiene varios ejemplares, cada ejemplar tiene su código aparte y se prestan independientemente"

Nota: Puedes acceder al archivo "01-contexto\brief-cliente.md" Ya que de aca fue que realice el trabajo de las especificaciones

c5: Saca las concluciones dependiendo de "los estudiantes a veces piden renovar el préstamo. La renovación les da otros 15 días (o 3 días si era alta demanda). Pero la renovación solo se puede hacer si nadie más ha solicitado ese libro mientras tanto. Si otro estudiante lo está esperando, no se renueva, hay que devolverlo"
```

---

### Resumen de la respuesta de la IA

Leyó `01-contexto/brief-cliente.md` para confirmar el contexto. Consolidó las 5 decisiones: pregrado=3/postgrado=5, `estado` agregado a Ejemplar, `estado`+`fecha_pago` agregados a Multa, Ejemplar definido como copia física individual (eliminando `cantidad`), y derivó la RN8 (renovación bloqueada si hay `SolicitudReserva` activa para el libro). Presentó el árbol de carpetas de 4 capas (models, db, repositories, services, api) y esperó aprobación antes de escribir código.

---

### Mi evaluación

**¿La respuesta cumplió con lo que pedí?**

- [x] Completamente.

**¿La acepté tal cual o la modifiqué?**

- [x] Tal cual.

**¿Qué aprendí de esta interacción?**

> Darle acceso al brief original (c5) fue más eficiente que intentar describir yo mismo la regla. La IA extrajo la regla de renovación correctamente sin que yo tuviera que formalizarla.

---

## Notas para el siguiente prompt

- El árbol propuesto tiene 5 capas. Si se quiere una arquitectura más limpia y profesional, pedirla explícitamente en el siguiente prompt.
