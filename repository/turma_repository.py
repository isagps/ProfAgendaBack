from config.globals import db
from entity.horario import Horario
from entity.materia import Materia
from entity.professor import Professor
from entity.turma import Turma
from exception.error_execution import ErrorExecution
from infrastructure.base_repository import BaseRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging

class TurmaRepository(BaseRepository[Turma]):
    """
    Repositório responsável pelas operações de atualização da entidade Turma no banco de dados.
    Herda de BaseRepository para fornecer métodos CRUD genéricos, e implementa um método 
    de atualização customizado.
    """

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Turma]:
        """
        Atualiza uma instância de Turma com base nos dados fornecidos. 
        Se a turma com o ID especificado não for encontrada, uma exceção é levantada.
        
        Args:
            id (int): ID da Turma a ser atualizada.
            data (Dict[str, Any]): Dados a serem atualizados, incluindo nome da turma e horários.
        
        Returns:
            Optional[Turma]: A turma atualizada, ou None se ocorrer um erro.
        
        Raises:
            ErrorExecution: Se a turma ou os dados de professor/matéria forem inválidos.
            TypeError: Se o parâmetro `data` não for um dicionário.
        """
        session: Session = db.session
        try:
            if not isinstance(data, dict):
                raise TypeError("O parâmetro 'data' deve ser um dicionário")

            turma = session.get(Turma, id)
            if not turma:
                raise ErrorExecution(f"Registro com ID {id} não encontrado para atualização")

            # Atualiza o nome da turma se estiver nos dados
            if 'nome' in data:
                turma.nome = data['nome']

            # Atualiza os horários da turma se fornecidos
            if 'horarios' in data:
                self._atualizar_horarios(session, turma, data['horarios'])

            session.commit()
            session.refresh(turma)
            return turma
        except (SQLAlchemyError, ValueError, TypeError) as e:
            session.rollback()
            logging.error(f"Erro em update da Turma: {str(e)}")
            raise ErrorExecution(e)

    def _atualizar_horarios(self, session: Session, turma: Turma, horarios_data: list) -> None:
        """
        Atualiza a lista de horários de uma turma. Primeiro limpa todos os horários existentes 
        e depois adiciona os novos horários fornecidos.

        Args:
            session (Session): Sessão atual do banco de dados.
            turma (Turma): Instância da turma a ser atualizada.
            horarios_data (list): Lista de dados contendo os novos horários para a turma.
        
        Raises:
            ErrorExecution: Se os dados de professor ou matéria forem inválidos.
        """
        # Remove todos os horários antigos da turma
        turma.horarios.clear()

        # Adiciona novos horários com base nos dados fornecidos
        for horario_data in horarios_data:
            professor, materia = self._buscar_professor_e_materia(session, horario_data)
            
            # Cria uma nova instância de Horario e a adiciona à turma
            novo_horario = Horario(
                dia_da_semana=horario_data['dia_da_semana'],
                hora=horario_data['hora'],
                professor=professor,
                materia=materia,
                turma=turma
            )
            turma.horarios.append(novo_horario)

    def _buscar_professor_e_materia(self, session: Session, horario_data: Dict[str, Any]) -> tuple:
        """
        Busca e valida a instância do professor e da matéria com base nos dados fornecidos. 
        Verifica se o professor existe e se a matéria está vinculada ao professor.

        Args:
            session (Session): Sessão atual do banco de dados.
            horario_data (Dict[str, Any]): Dados do horário contendo IDs de professor e matéria.
        
        Returns:
            tuple: Uma tupla contendo as instâncias de Professor e Matéria.

        Raises:
            ErrorExecution: Se o professor ou matéria não forem encontrados, ou se a matéria
                            não estiver vinculada ao professor.
        """
        professor_id = horario_data['professor']['id']
        professor = session.get(Professor, professor_id)
        if not professor:
            raise ErrorExecution(f"Professor com ID {professor_id} não encontrado")

        materia_id = horario_data['materia']['id']
        materia = session.get(Materia, materia_id)
        if not materia:
            raise ErrorExecution(f"Matéria com ID {materia_id} não encontrada")

        # Verificar se a matéria está vinculada ao professor
        if materia not in professor.materias:
            raise ErrorExecution(f"A matéria '{materia.nome}' não está vinculada ao professor '{professor.nome}'")

        return professor, materia