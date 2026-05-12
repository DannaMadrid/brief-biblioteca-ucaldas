from pydantic import BaseModel


class EjemplarResponse(BaseModel):
    id: str
    cod_libro: str
    estado: str
