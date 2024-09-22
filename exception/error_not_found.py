from infrastructure.base_error import BaseError

class ErrorNotFound(BaseError):
    """
    Exceção levantada quando um objeto solicitado não é encontrado.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão de erro usada quando não é fornecida uma mensagem personalizada.
    """
    DEFAULT_MESSAGE = "Objeto não encontrado."