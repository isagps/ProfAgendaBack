from entity.professor import Professor
from infrastructure.base_service import BaseService
from repository.professor_repository import ProfessorRepository

class ProfessorService(BaseService[Professor]):
    """
    Serviço responsável por gerenciar operações relacionadas à entidade Professor.

    Esta classe herda de BaseService, que fornece métodos CRUD padrão. O ProfessorService
    utiliza o ProfessorRepository para interagir com a camada de dados.

    Métodos herdados:
        - get_by_id
        - get_all
        - create
        - update
        - delete
    """
    def __init__(self):
        """
        Inicializa o ProfessorService com o repositório específico de Professor.
        """
        super().__init__(ProfessorRepository())