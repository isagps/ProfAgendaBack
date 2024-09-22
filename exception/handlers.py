from exception.error_creation import ErrorCreation
from exception.error_delete import ErrorDelete
from exception.error_execution import ErrorExecution
from exception.error_invalid_object import ErrorInvalidObject
from exception.error_not_found import ErrorNotFound
from exception.error_object_already_exists import ErrorObjectAlreadyExist
from exception.error_update import ErrorUpdate
from flask import jsonify

class ErrorHandlerRegistry:
    """
    Classe responsável por registrar handlers de erro personalizados para a aplicação Flask.
    
    Esta classe registra handlers de erro para exceções específicas, como `ErrorExecution`, `ErrorNotFound`, `ErrorCreation`,
    entre outras. Para cada erro tratado, uma resposta JSON padronizada é retornada ao cliente, com a mensagem de erro apropriada
    e o código de status HTTP correspondente.
    """

    def __init__(self, app):
        """
        Inicializa o registrador de handlers de erro.

        Args:
            app (Flask): A instância da aplicação Flask onde os handlers de erro serão registrados.
        """
        self.app = app
        self.register_error_handlers()

    def register_error_handlers(self):
        """
        Registra os handlers de erro na aplicação Flask.
        """
        self.app.errorhandler(Exception)(self.handle_generic_error)
        self.app.errorhandler(ErrorExecution)(self.handle_execution_error)
        self.app.errorhandler(ErrorNotFound)(self.handle_not_found_error)
        self.app.errorhandler(ErrorCreation)(self.handle_creation_error)
        self.app.errorhandler(ErrorObjectAlreadyExist)(self.handle_object_already_exist_error)
        self.app.errorhandler(ErrorInvalidObject)(self.handle_invalid_object)
        self.app.errorhandler(ErrorUpdate)(self.handle_update_error)
        self.app.errorhandler(ErrorDelete)(self.handle_deletion_error)

    @staticmethod
    def create_error_response(error, default_message, status_code):
        """
        Cria uma resposta de erro JSON padronizada e registra o erro nos logs.

        Args:
            error (Exception): A exceção que foi capturada.
            default_message (str): A mensagem padrão a ser retornada no caso de erro.
            status_code (int): O código de status HTTP a ser retornado.

        Retorna:
            Tuple[Response, int]: Uma resposta JSON contendo a mensagem de erro e o status code.
        """
        response = jsonify({'message': error.message})
        response.status_code = status_code
        return response

    def handle_generic_error(self, error: Exception):
        """
        Manipula exceções genéricas não tratadas.

        Retorna:
            500 Internal Server Error com uma mensagem de erro padrão.
        """
        return self.create_error_response(error, 'Erro desconhecido interno do servidor, por favor entre em contato com o suporte.', 500)

    def handle_execution_error(self, error: ErrorExecution):
        """
        Manipula erros internos de execução.

        Retorna:
            500 Internal Server Error com uma mensagem padrão de erro de execução.
        """
        return self.create_error_response(error, ErrorExecution.DEFAULT_MESSAGE, 500)

    def handle_not_found_error(self, error: ErrorNotFound):
        """
        Manipula erros de recursos não encontrados.

        Retorna:
            404 Not Found com uma mensagem padrão de "não encontrado".
        """
        return self.create_error_response(error, ErrorNotFound.DEFAULT_MESSAGE, 404)

    def handle_creation_error(self, error: ErrorCreation):
        """
        Manipula erros ao criar objetos.

        Retorna:
            400 Bad Request com uma mensagem padrão de erro de criação.
        """
        return self.create_error_response(error, ErrorCreation.DEFAULT_MESSAGE, 400)

    def handle_object_already_exist_error(self, error: ErrorObjectAlreadyExist):
        """
        Manipula erros onde o objeto já existe no sistema.

        Retorna:
            400 Bad Request com uma mensagem padrão de "objeto já existe".
        """
        return self.create_error_response(error, ErrorObjectAlreadyExist.DEFAULT_MESSAGE, 400)

    def handle_invalid_object(self, error: ErrorInvalidObject):
        """
        Manipula erros de objetos inválidos.

        Retorna:
            400 Bad Request com uma mensagem padrão de "objeto inválido".
        """
        return self.create_error_response(error, ErrorInvalidObject.DEFAULT_MESSAGE, 400)

    def handle_update_error(self, error: ErrorUpdate):
        """
        Manipula erros ao atualizar objetos.

        Retorna:
            400 Bad Request com uma mensagem padrão de erro de atualização.
        """
        return self.create_error_response(error, ErrorUpdate.DEFAULT_MESSAGE, 400)

    def handle_deletion_error(self, error: ErrorDelete):
        """
        Manipula erros ao deletar objetos.

        Retorna:
            400 Bad Request com uma mensagem padrão de erro de deleção.
        """
        return self.create_error_response(error, ErrorDelete.DEFAULT_MESSAGE, 400)