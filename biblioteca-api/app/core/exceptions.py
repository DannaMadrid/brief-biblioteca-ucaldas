class BibliotecaException(Exception):
    def __init__(self, mensaje: str, codigo_error: str = "error"):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(mensaje)


class EntidadNoEncontrada(BibliotecaException):
    pass


class ConflictoDeNegocio(BibliotecaException):
    pass


class DatosInvalidos(BibliotecaException):
    pass
