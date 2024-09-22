from infrastructure.base_error import BaseError

class ErrorObjectAlreadyExist(BaseError):
    """
    Exceção levantada quando se tenta criar um objeto que já existe.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão de erro usada quando não é fornecida uma mensagem personalizada.
    """
    DEFAULT_MESSAGE = "Um objeto com esses dados já existe."