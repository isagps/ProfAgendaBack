from .horario_controller import horario_blueprint
from .professor_controller import professor_blueprint
from .turma_controller import turma_blueprint
from controller.materia_controller import materia_blueprint

def register_blueprints(app):
    """
    Registra os blueprints das rotas no aplicativo Flask.

    Esta função agrega todos os blueprints definidos para as diferentes entidades
    (horário, matéria, professor, turma) e os registra no aplicativo Flask.

    Args:
        app (Flask): A instância do aplicativo Flask onde os blueprints serão registrados.

    Blueprints Registrados:
        - horario_blueprint: Rotas relacionadas à entidade Horario.
        - materia_blueprint: Rotas relacionadas à entidade Materia.
        - professor_blueprint: Rotas relacionadas à entidade Professor.
        - turma_blueprint: Rotas relacionadas à entidade Turma.
    """
    # Lista contendo todos os blueprints a serem registrados
    blueprints = [
        horario_blueprint,
        materia_blueprint,
        professor_blueprint,
        turma_blueprint
    ]
    
    # Registra cada blueprint na instância do aplicativo Flask
    for blueprint in blueprints:
        app.register_blueprint(blueprint)