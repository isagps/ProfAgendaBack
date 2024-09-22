from config.globals import db
from entity.relations import professor_materia
from infrastructure.base_entity import BaseEntity
from typing import Dict, Optional, Set

class Professor(BaseEntity):
    """
    Representa a entidade Professor no banco de dados.

    Atributos:
        nome (str): Nome do professor, obrigatório.
        materias (List[Materia]): Relação muitos-para-muitos com a entidade Materia.
        horarios (List[Horario]): Relação um-para-muitos com a entidade Horario.
    """
    __tablename__ = 'professor'

    nome = db.Column(db.String(128), nullable=False)
    materias = db.relationship('Materia', secondary=professor_materia, back_populates='professores')
    horarios = db.relationship('Horario', back_populates='professor')

    def to_dict(self, visited: Optional[Set[int]] = None, max_depth: int = 5, current_depth: int = 0) -> Dict:
        """
        Converte o objeto Professor em um dicionário.

        Args:
            visited (Optional[Set[int]]): Objetos já visitados para evitar loops de referência.
            max_depth (int): Profundidade máxima para serialização de relacionamentos.
            current_depth (int): Profundidade atual da serialização.

        Returns:
            Dict: Representação em dicionário do objeto Professor.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'materias': [
                {
                    'id': materia.id,
                    'nome': materia.nome,
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
                        for horario in self.horarios if horario.materia_id == materia.id
                    ]
                }
                for materia in self.materias
            ]
        }