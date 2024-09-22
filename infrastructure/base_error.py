class BaseError(Exception):
    """
    Classe base para exceções personalizadas.

    Esta classe serve como base para outras exceções personalizadas que herdam dela. Ela permite
    que cada exceção tenha uma mensagem padrão, que pode ser substituída por uma mensagem personalizada
    ao lançar a exceção.

    Atributos:
        DEFAULT_MESSAGE (str): A mensagem padrão usada quando nenhuma mensagem personalizada é fornecida.

    Métodos:
        __init__(message: str = None):
            Inicializa a exceção com uma mensagem personalizada ou a mensagem padrão.
    """

    DEFAULT_MESSAGE = "Ocorreu um erro."

    def __init__(self, message: str = None):
        """
        Inicializa a exceção com uma mensagem personalizada ou com a mensagem padrão.

        Args:
            message (str, opcional): Mensagem personalizada para a exceção. Se não for fornecida, 
                                     será usada a mensagem padrão definida no atributo `DEFAULT_MESSAGE`.
        """
        self.message = message or self.DEFAULT_MESSAGE
        super().__init__(self.message)