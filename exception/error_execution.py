from infrastructure.base_error import BaseError

class ErrorExecution(BaseError):
    """
    Exceção levantada quando ocorre um erro desconhecido durante a execução de uma operação.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão de erro usada quando não é fornecida uma mensagem personalizada.
    """
    DEFAULT_MESSAGE = "Erro desconhecido."