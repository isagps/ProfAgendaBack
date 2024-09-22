from entity.materia import Materia
from infrastructure.base_service import BaseService
from repository.materia_repository import MateriaRepository

class MateriaService(BaseService[Materia]):
    """
    Serviço responsável por gerenciar operações relacionadas à entidade Materia.

    Esta classe herda de BaseService, que fornece métodos CRUD padrão. O MateriaService
    utiliza o MateriaRepository para interagir com a camada de dados.

    Métodos herdados:
        - get_by_id
        - get_all
        - create
        - update
        - delete
    """
    def __init__(self):
        """
        Inicializa o MateriaService com o repositório específico de Materia.
        """
        super().__init__(MateriaRepository())