from infrastructure.base_error import BaseError

class ErrorUpdate(BaseError):
    """
    Exceção levantada quando ocorre uma falha ao atualizar um objeto.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão de erro usada quando não é fornecida uma mensagem personalizada.
    """
    DEFAULT_MESSAGE = "Falha ao atualizar o objeto."