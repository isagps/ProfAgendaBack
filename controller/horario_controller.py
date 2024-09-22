from entity.horario import Horario
from infrastructure.base_controller import BaseController
from service.horario_service import HorarioService

class HorarioController(BaseController[Horario]):
    """
    Controller responsável pelas operações relacionadas à entidade Horario.

    Herda de BaseController, utilizando a entidade Horario e o serviço
    HorarioService para realizar as operações padrão (CRUD).

    Atributos:
        blueprint: O blueprint do controlador, utilizado para definir rotas relacionadas à entidade Horario.
    """
    def __init__(self):
        """
        Inicializa o HorarioController, passando o HorarioService e o nome 'horario' para o BaseController.
        """
        super().__init__(HorarioService, 'horario')

# Instância do blueprint de HorarioController para ser registrado nas rotas
horario_blueprint = HorarioController().blueprint