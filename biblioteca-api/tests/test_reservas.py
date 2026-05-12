def test_crear_reserva_exitosa(client, estudiante_pregrado, libro_normal):
    resp = client.post("/reservas", json={"estudiante_codigo": "EST-001", "libro_codigo": "LIB-001"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["estado"] == "activa"
    assert data["estudiante_codigo"] == "EST-001"
    assert data["libro_codigo"] == "LIB-001"


def test_crear_reserva_duplicada(client, estudiante_pregrado, libro_normal):
    client.post("/reservas", json={"estudiante_codigo": "EST-001", "libro_codigo": "LIB-001"})
    resp = client.post("/reservas", json={"estudiante_codigo": "EST-001", "libro_codigo": "LIB-001"})
    assert resp.status_code == 409
    assert resp.json()["error"] == "reserva_duplicada"


def test_crear_reserva_estudiante_no_encontrado(client, libro_normal):
    resp = client.post("/reservas", json={"estudiante_codigo": "NO-EXISTE", "libro_codigo": "LIB-001"})
    assert resp.status_code == 404


def test_crear_reserva_libro_no_encontrado(client, estudiante_pregrado):
    resp = client.post("/reservas", json={"estudiante_codigo": "EST-001", "libro_codigo": "NO-EXISTE"})
    assert resp.status_code == 404
