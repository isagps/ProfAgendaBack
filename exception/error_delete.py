from infrastructure.base_error import BaseError

class ErrorDelete(BaseError):
    """
    Exceção levantada quando ocorre uma falha ao deletar um objeto.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão de erro usada quando não é fornecida uma mensagem personalizada.
    """
    DEFAULT_MESSAGE = "Falha ao deletar o objeto."