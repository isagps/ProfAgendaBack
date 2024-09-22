from config.globals import db
from infrastructure.base_entity import BaseEntity
from typing import Dict, Optional, Set

class Turma(BaseEntity):
    """
    A classe Turma representa uma entidade no banco de dados, associada à tabela 'turma'.
    
    Atributos:
        __tablename__ (str): Nome da tabela no banco de dados.
        nome (db.Column): Nome da turma, que é único e obrigatório.
        horarios (db.relationship): Relacionamento com a tabela "Horario", com uma 
                                    associação bi-direcional e uma política de 
                                    deleção em cascata.

    Métodos:
        to_dict(visited: Optional[Set[int]], max_depth: int, current_depth: int) -> Dict:
            Retorna uma representação em dicionário da entidade, incluindo os 
            relacionamentos com Horário, Materia e Professor.
    """
    
    __tablename__ = 'turma'
    
    nome = db.Column(db.String(128), nullable=False, unique=True)
    horarios = db.relationship("Horario", back_populates="turma", cascade="all, delete-orphan")
    
    def to_dict(self, visited: Optional[Set[int]] = None, max_depth: int = 5, current_depth: int = 0) -> Dict:
        """
        Converte a instância da turma em um dicionário, incluindo seus relacionamentos
        com horários, matérias e professores.

        Args:
            visited (Optional[Set[int]]): Conjunto opcional para evitar ciclos em 
                                          relacionamentos de entidades.
            max_depth (int): Profundidade máxima para evitar carregamento excessivo 
                             de dados aninhados.
            current_depth (int): Profundidade atual da recursão.

        Returns:
            Dict: Representação em dicionário da turma, incluindo seus horários, 
                  matérias e professores.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "horarios": [
                {
                    "id": horario.id,
                    "dia_da_semana": horario.dia_da_semana,
                    "hora": horario.hora,
                    "materia": {
                        "id": horario.materia.id,
                        "nome": horario.materia.nome
                    },
                    "professor": {
                        "id": horario.professor.id,
                        "nome": horario.professor.nome
                    },
                }
                for horario in self.horarios
            ]
        }