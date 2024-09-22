from entity.turma import Turma
from infrastructure.base_controller import BaseController
from service.turma_service import TurmaService

class TurmaController(BaseController[Turma]):
    """
    Controller responsável pelas operações relacionadas à entidade Turma.

    Herda de BaseController, utilizando a entidade Turma e o serviço
    TurmaService para realizar as operações padrão (CRUD).

    Atributos:
        blueprint: O blueprint do controlador, utilizado para definir rotas relacionadas à entidade Turma.
    """
    def __init__(self):
        """
        Inicializa o TurmaController, passando o TurmaService e o nome 'turma' para o BaseController.
        """
        super().__init__(TurmaService, 'turma')

# Instância do blueprint de TurmaController para ser registrado nas rotas
turma_blueprint = TurmaController().blueprint