from config.globals import db
from entity.materia import Materia
from entity.professor import Professor
from exception.error_execution import ErrorExecution
from infrastructure.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging

class ProfessorRepository(BaseRepository[Professor]):
    """
    Repositório específico para o modelo `Professor`.

    Esta classe herda todas as funcionalidades da classe `BaseRepository` e
    está preparada para realizar operações CRUD (Create, Read, Update, Delete)
    no modelo `Professor`.

    Args:
        BaseRepository (Generic[T]): Classe base genérica para repositórios.
    """

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Professor]:
        """
        Atualiza os dados de um professor existente.

        Parâmetros:
            id (int): Identificador único do professor a ser atualizado.
            data (Dict[str, Any]): Dicionário contendo os campos a serem atualizados.
                - 'nome' (str, opcional): Novo nome do professor.
                - 'materias' (List[Dict[str, int]], opcional): Lista de dicionários contendo
                  os IDs das matérias associadas ao professor. Cada dicionário deve ter a chave 'id'.

        Retorna:
            Optional[Professor]: O objeto Professor atualizado, ou None se não for encontrado.

        Exceções:
            TypeError: Se o parâmetro 'data' não for um dicionário ou se 'materias' não for uma lista de dicionários com 'id'.
            ValueError: Se algum dicionário em 'materias' não contiver a chave 'id'.
            ErrorExecution: Se o professor não for encontrado ou se algumas matérias fornecidas não forem encontradas.
            SQLAlchemyError: Erros relacionados ao banco de dados durante a operação.
        """
        if not isinstance(data, dict):
            raise TypeError("O parâmetro 'data' deve ser um dicionário")

        session: Session = db.session
        try:
            professor = session.get(Professor, id)
            if not professor:
                raise ErrorExecution(f"Registro com ID {id} não encontrado para atualização")

            if 'nome' in data:
                professor.nome = data['nome']

            if 'materias' in data:
                if not isinstance(data['materias'], list):
                    raise TypeError("'materias' deve ser uma lista de dicionários com 'id'")

                # Extrai os IDs das matérias fornecidas
                materia_ids = [m['id'] for m in data['materias'] if isinstance(m, dict) and 'id' in m]
                if len(materia_ids) != len(data['materias']):
                    raise ValueError("Cada matéria deve ser um dicionário contendo o campo 'id'")

                # Busca as matérias no banco de dados
                materias = session.query(Materia).filter(Materia.id.in_(materia_ids)).all()
                if len(materias) != len(materia_ids):
                    raise ErrorExecution("Algumas matérias fornecidas não foram encontradas")

                # Atualiza a associação de matérias do professor
                professor.materias = materias

            session.commit()
            session.refresh(professor)
            return professor

        except (SQLAlchemyError, ValueError, TypeError) as e:
            session.rollback()
            logging.error(f"Erro em update do Professor: {e}")
            raise ErrorExecution(e)