from config.globals import db
from entity.relations import professor_materia
from infrastructure.base_entity import BaseEntity
from typing import Dict, Optional, Set

class Materia(BaseEntity):
    """
    Representa a entidade Materia no banco de dados.

    Atributos:
        nome (str): Nome da matéria, único e obrigatório.
        professores (List[Professor]): Relação muitos-para-muitos com a entidade Professor.
        horarios (List[Horario]): Relação um-para-muitos com a entidade Horario.
    """
    __tablename__ = 'materia'

    nome = db.Column(db.String(128), nullable=False, unique=True)
    professores = db.relationship('Professor', secondary=professor_materia, back_populates='materias')
    horarios = db.relationship('Horario', back_populates='materia')

    def to_dict(self, visited: Optional[Set[int]] = None, max_depth: int = 5, current_depth: int = 0) -> Dict:
        """
        Converte o objeto Materia em um dicionário.

        Args:
            visited (Optional[Set[int]]): Objetos já visitados para evitar loops de referência.
            max_depth (int): Profundidade máxima para serialização de relacionamentos.
            current_depth (int): Profundidade atual da serialização.

        Returns:
            Dict: Representação em dicionário do objeto Materia.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'professores': [
                {
                    'id': professor.id,
                    'nome': professor.nome,
                    'horarios': [
                        {
                            'id': horario.id,
                            'dia_da_semana': horario.dia_da_semana,
                            'hora': horario.hora,
                            'turma': {
                                'id': horario.turma.id,
                                'nome': horario.turma.nome
                            }
                        }
                        for horario in professor.horarios if horario.materia_id == self.id
                    ]
                }
                for professor in self.professores
            ]
        }