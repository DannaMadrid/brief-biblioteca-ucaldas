# API Sistema de Préstamos — Biblioteca Universidad de Caldas

API REST construida con **FastAPI** para gestionar préstamos, devoluciones, multas y reservas de libros.

## Requisitos

- Python 3.11+

## Instalación

```bash
pip install -r requirements.txt
```

## Levantar el servidor

```bash
uvicorn main:app --reload
```

El servidor arranca en `http://localhost:8000`.

- Documentación interactiva: `http://localhost:8000/docs`
- Documentación alternativa: `http://localhost:8000/redoc`

## Ejecutar tests

```bash
pytest
```

## Estructura del proyecto

```
biblioteca-api/
├── app/
│   ├── core/           ← excepciones de dominio
│   ├── models/         ← entidades del negocio (Pydantic)
│   ├── db/             ← almacén en memoria + datos semilla
│   ├── repositories/   ← acceso a datos (CRUD)
│   ├── services/       ← lógica de negocio (RN1–RN8)
│   └── api/
│       ├── schemas/    ← contratos JSON de request/response
│       └── routers/    ← endpoints HTTP
└── tests/
```

## Reglas de negocio implementadas

| Regla | Descripción |
|---|---|
| RN1 | Pregrado: máx. 3 préstamos activos. Posgrado: máx. 5. |
| RN2 | Bloqueo si el estudiante tiene préstamos vencidos sin devolver. |
| RN3 | Bloqueo si el estudiante tiene multas pendientes de pago. |
| RN4 | El ejemplar debe estar disponible para prestarse. |
| RN5 | Alta demanda: plazo 3 días. Normal: plazo 15 días. |
| RN6 | Solo se devuelven préstamos con estado `activo`. |
| RN7 | Multa de $2.000/día por devolución tardía. |
| RN8 | Renovación bloqueada si hay reservas activas para el libro. |
