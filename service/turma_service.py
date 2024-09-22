from entity.turma import Turma
from infrastructure.base_service import BaseService
from repository.turma_repository import TurmaRepository

class TurmaService(BaseService[Turma]):
    """
    Serviço responsável por gerenciar operações relacionadas à entidade Turma.

    Esta classe herda de BaseService, que fornece métodos CRUD padrão. O TurmaService
    utiliza o TurmaRepository para interagir com a camada de dados.

    Métodos herdados:
        - get_by_id
        - get_all
        - create
        - update
        - delete
    """
    def __init__(self):
        """
        Inicializa o TurmaService com o repositório específico de Turma.
        """
        super().__init__(TurmaRepository())