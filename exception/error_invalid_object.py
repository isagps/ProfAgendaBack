from infrastructure.base_error import BaseError

class ErrorInvalidObject(BaseError):
    """
    Exceção levantada quando um objeto inválido é fornecido.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão de erro usada quando não é fornecida uma mensagem personalizada.
    """
    DEFAULT_MESSAGE = "Objeto inválido."