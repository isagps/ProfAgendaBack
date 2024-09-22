from entity.materia import Materia
from infrastructure.base_controller import BaseController
from service.materia_service import MateriaService

class MateriaController(BaseController[Materia]):
    """
    Controller responsável pelas operações relacionadas à entidade Materia.

    Herda de BaseController, utilizando a entidade Materia e o serviço
    MateriaService para realizar as operações padrão (CRUD).

    Atributos:
        blueprint: O blueprint do controlador, utilizado para definir rotas relacionadas à entidade Materia.
    """
    def __init__(self):
        """
        Inicializa o MateriaController, passando o MateriaService e o nome 'materia' para o BaseController.
        """
        super().__init__(MateriaService, 'materia')

# Instância do blueprint de MateriaController para ser registrado nas rotas
materia_blueprint = MateriaController().blueprint