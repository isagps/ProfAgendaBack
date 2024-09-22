from entity.horario import Horario
from infrastructure.base_service import BaseService
from repository.horario_repository import HorarioRepository

class HorarioService(BaseService[Horario]):
    """
    Serviço responsável por gerenciar operações relacionadas à entidade Horario.

    Esta classe herda de BaseService, que fornece métodos CRUD padrão. O HorarioService
    utiliza o HorarioRepository para interagir com a camada de dados.

    Métodos herdados:
        - get_by_id
        - get_all
        - create
        - update
        - delete
    """
    def __init__(self):
        """
        Inicializa o HorarioService com o repositório específico de Horario.
        """
        super().__init__(HorarioRepository())