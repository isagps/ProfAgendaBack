from entity.professor import Professor
from infrastructure.base_controller import BaseController
from service.professor_service import ProfessorService

class ProfessorController(BaseController[Professor]):
    """
    Controller responsável pelas operações relacionadas à entidade Professor.

    Herda de BaseController, utilizando a entidade Professor e o serviço
    ProfessorService para realizar as operações padrão (CRUD).

    Atributos:
        blueprint: O blueprint do controlador, utilizado para definir rotas relacionadas à entidade Professor.
    """
    def __init__(self):
        """
        Inicializa o ProfessorController, passando o ProfessorService e o nome 'professor' para o BaseController.
        """
        super().__init__(ProfessorService, 'professor')

# Instância do blueprint de ProfessorController para ser registrado nas rotas
professor_blueprint = ProfessorController().blueprint