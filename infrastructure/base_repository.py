from config.globals import db
from exception.error_execution import ErrorExecution
from exception.error_invalid_object import ErrorInvalidObject
from exception.error_object_already_exists import ErrorObjectAlreadyExist
from infrastructure.base_model import BaseModel
from model.page import Page
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from typing import Type, TypeVar, Generic, Optional, Dict, Any, List
import logging

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """
    Repositório genérico para operações CRUD (Create, Read, Update, Delete) utilizando SQLAlchemy.

    Esta classe fornece métodos básicos para interagir com o banco de dados para qualquer modelo que herde de `BaseModel`.
    Ela abstrai operações comuns, facilitando a reutilização e mantendo o código DRY (Don't Repeat Yourself).

    Args:
        Generic (T): Tipo genérico que deve ser uma subclasse de `BaseModel`.

    Attributes:
        model (Type[T]): O modelo SQLAlchemy associado ao repositório.
        _logger (logging.Logger): Logger para registrar informações e erros.
    """

    _logger: logging.Logger

    def __init__(self):
        """
        Inicializa o repositório com o modelo específico e configura o logger.
        """
        self.model: Type[T] = self.__orig_bases__[0].__args__[0]
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_by_id(self, id: int, relationships: Optional[List[str]] = None) -> Optional[T]:
        """
        Recupera um registro pelo seu ID, opcionalmente carregando relacionamentos especificados.

        Args:
            id (int): ID do registro a ser recuperado.
            relationships (Optional[List[str]]): Lista de nomes de relacionamentos a serem carregados.

        Returns:
            Optional[T]: Instância do modelo correspondente ao ID fornecido ou `None` se não encontrado.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da consulta.
        """
        session: Session = db.session
        try:
            query = session.query(self.model)
            if relationships:
                for rel in relationships:
                    query = query.options(joinedload(rel))
            result = query.get(id)
            return result
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em get_by_id: {str(e)}")
            raise ErrorExecution(e)

    def get_all(self, page_number: int = 1, page_size: int = 10, filter_str: Optional[str] = None) -> Page:
        """
        Recupera todos os registros com suporte a paginação e filtragem por string.

        Args:
            page_number (int, optional): Número da página a ser recuperada. Padrão é 1.
            page_size (int, optional): Número de itens por página. Padrão é 10.
            filter_str (Optional[str], optional): String para filtrar os registros. Filtra em colunas de string.

        Returns:
            Page: Objeto `Page` contendo os registros, informações de paginação e total de itens.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da consulta.
        """
        session: Session = db.session
        try:
            query = session.query(self.model)
            if filter_str:
                filter_clauses = [
                    column.ilike(f'%{filter_str}%') 
                    for column in self.model.__table__.columns 
                    if hasattr(column.type, 'python_type') and issubclass(column.type.python_type, str)
                ]
                if filter_clauses:
                    query = query.filter(db.or_(*filter_clauses))
            total_items = query.count()
            records = query.offset((page_number - 1) * page_size).limit(page_size).all()
            return Page(records, page_number, page_size, total_items)
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em get_all: {str(e)}")
            raise ErrorExecution(e)

    def get_all_without_pagination(self) -> List[T]:
        """
        Recupera todos os registros sem aplicar paginação.

        Returns:
            List[T]: Lista de instâncias do modelo.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da consulta.
        """
        session: Session = db.session
        try:
            records = session.query(self.model).all()
            return records
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em get_all_without_pagination: {str(e)}")
            raise ErrorExecution(e)

    def create(self, data: Dict[str, Any]) -> Optional[T]:
        """
        Cria um novo registro no banco de dados.

        Args:
            data (Dict[str, Any]): Dicionário contendo os dados para criar o registro.

        Returns:
            Optional[T]: Instância do modelo recém-criado ou `None` se falhar.

        Raises:
            ErrorObjectAlreadyExist: Se violar a restrição de unicidade.
            ErrorInvalidObject: Se violar a restrição de verificação (CHECK).
            ErrorExecution: Para outros erros de execução.
        """
        session: Session = db.session
        try:
            new_record = self.model(**data)
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            return new_record
        except IntegrityError as e:
            session.rollback()
            error_message = str(e.orig)
            self._logger.error(f"Erro de integridade em create: {error_message}")
            if 'UNIQUE constraint failed' in error_message:
                raise ErrorObjectAlreadyExist(e)
            elif 'CHECK constraint failed' in error_message:
                raise ErrorInvalidObject(e)
            else:
                raise ErrorExecution(e)
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em create: {str(e)}")
            raise ErrorExecution(e)

    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """
        Atualiza um registro existente no banco de dados.

        Args:
            id (int): ID do registro a ser atualizado.
            data (Dict[str, Any]): Dicionário contendo os campos a serem atualizados.

        Returns:
            Optional[T]: Instância do modelo atualizado ou `None` se não encontrado.

        Raises:
            TypeError: Se `data` não for um dicionário.
            ErrorExecution: Se o registro não for encontrado ou ocorrer um erro durante a atualização.
        """
        session: Session = db.session
        try:
            if not isinstance(data, dict):
                raise TypeError("O parâmetro 'data' deve ser um dicionário")

            record = session.get(self.model, id)
            if not record:
                raise ErrorExecution(f"Registro com ID {id} não encontrado para atualização")

            for key, value in data.items():
                if hasattr(self.model, key) and key != 'materias':
                    setattr(record, key, value)

            session.commit()
            session.refresh(record)
            return record
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em update: {str(e)}")
            raise ErrorExecution(e)

    def delete(self, id: int) -> bool:
        """
        Deleta um registro do banco de dados pelo seu ID.

        Args:
            id (int): ID do registro a ser deletado.

        Returns:
            bool: `True` se o registro foi deletado com sucesso, `False` se não encontrado.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a deleção.
        """
        session: Session = db.session
        try:
            record = session.get(self.model, id)
            if record:
                session.delete(record)
                session.commit()
                self._logger.info(f"Registro com ID {id} deletado com sucesso.")
                return True
            self._logger.warning(f"Registro com ID {id} não encontrado para deleção.")
            return False
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em delete: {str(e)}")
            raise ErrorExecution(e)

    def count_all(self) -> int:
        """
        Conta o número total de registros na entidade.

        Returns:
            int: O número total de registros.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da consulta.
        """
        session: Session = db.session
        try:
            total_count = session.query(self.model).count()
            return total_count
        except SQLAlchemyError as e:
            session.rollback()
            self._logger.error(f"Erro em count_all: {str(e)}")
            raise ErrorExecution(e)