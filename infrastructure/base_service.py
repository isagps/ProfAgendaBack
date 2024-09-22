from exception.error_creation import ErrorCreation
from exception.error_delete import ErrorDelete
from exception.error_execution import ErrorExecution
from exception.error_invalid_object import ErrorInvalidObject
from exception.error_not_found import ErrorNotFound
from exception.error_object_already_exists import ErrorObjectAlreadyExist
from exception.error_update import ErrorUpdate
from infrastructure.base_model import BaseModel
from infrastructure.base_repository import BaseRepository
from model.page import Page
from typing import Optional, TypeVar, Generic, Dict, Any, List
import logging

T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):
    """
    Classe base para serviços que lidam com operações CRUD genéricas.
    
    Esta classe implementa os métodos comuns a serem utilizados por serviços de várias entidades, como buscar,
    criar, atualizar e deletar itens, além de fornecer suporte para paginação e manipulação de exceções.
    """
    _logger: logging.Logger

    def __init__(self, repository: BaseRepository[T]):
        """
        Inicializa a classe BaseService com o repositório correspondente à entidade.

        Args:
            repository (BaseRepository[T]): O repositório responsável por interagir com a camada de dados.
        """
        self.repository = repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_by_id(self, id: int) -> Optional[T]:
        """
        Busca um item pelo ID.

        Args:
            id (int): O ID do item a ser buscado.

        Returns:
            Optional[T]: O item encontrado ou None caso não exista.

        Raises:
            ErrorNotFound: Se o item com o ID fornecido não for encontrado.
        """
        result = self.repository.get_by_id(id)
        if not result:
            self._log_and_raise_warning(ErrorNotFound, f'Item com ID {id} não foi encontrado.')
        self._logger.debug(f'Item encontrado: {result}')
        return result

    def get_all(self, page_number: int = 1, page_size: int = 10, filter_str: Optional[str] = None) -> Page:
        """
        Busca itens com paginação e filtro opcional.

        Args:
            page_number (int): Número da página para paginação.
            page_size (int): Número de itens por página.
            filter_str (Optional[str]): Filtro opcional para a busca.

        Returns:
            Page: Um objeto contendo a página com os itens e a contagem total.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da busca.
        """
        try:
            results = self.repository.get_all(page_number, page_size, filter_str)
            self._logger.debug(f'Total de itens encontrados: {results.total_items}')
            return results
        except Exception as e:
            self._log_and_raise_error(ErrorExecution, 'Erro ao buscar itens.', e)

    def get_all_without_pagination(self) -> List[T]:
        """
        Busca todos os itens sem paginação.

        Returns:
            List[T]: Lista de todos os itens.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da busca.
        """
        try:
            return self.repository.get_all_without_pagination()
        except Exception as e:
            self._log_and_raise_error(ErrorExecution, 'Erro ao buscar todos os itens.', e)

    def create(self, data: Dict[str, Any]) -> Optional[T]:
        """
        Cria um novo item.

        Args:
            data (Dict[str, Any]): Dados do novo item a ser criado.

        Returns:
            Optional[T]: O item criado ou None caso ocorra um erro.

        Raises:
            ErrorObjectAlreadyExist: Se o item já existir.
            ErrorCreation: Se ocorrer um erro durante a criação do item.
        """
        try:
            result = self.repository.create(data)
            self._logger.debug(f'Item criado com sucesso: {result}')
            return result
        except ErrorObjectAlreadyExist as e:
            self._log_and_raise_warning(ErrorObjectAlreadyExist, 'O item já existe.', e)
        except Exception as e:
            self._log_and_raise_error(ErrorCreation, 'Erro ao criar item.', e)

    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """
        Atualiza um item existente.

        Args:
            id (int): O ID do item a ser atualizado.
            data (Dict[str, Any]): Dados atualizados do item.

        Returns:
            Optional[T]: O item atualizado ou None caso o item não seja encontrado ou ocorra um erro.

        Raises:
            ErrorNotFound: Se o item com o ID fornecido não for encontrado.
            ErrorInvalidObject: Se os dados fornecidos para atualização forem inválidos.
            ErrorUpdate: Se ocorrer um erro durante a atualização.
        """
        try:
            result = self.repository.update(id, data)
            if result:
                self._logger.debug(f'Item atualizado com sucesso: {result}')
            else:
                self._log_and_raise_warning(ErrorNotFound, f'Item com ID {id} não foi encontrado para atualização.')
            return result
        except ErrorInvalidObject as e:
            self._log_and_raise_warning(ErrorInvalidObject, 'Dados inválidos fornecidos para atualização.', e)
        except Exception as e:
            self._log_and_raise_error(ErrorUpdate, 'Erro ao atualizar item.', e)

    def delete(self, id: int) -> bool:
        """
        Deleta um item pelo ID.

        Args:
            id (int): O ID do item a ser deletado.

        Returns:
            bool: True se o item foi deletado com sucesso, False se não foi encontrado.

        Raises:
            ErrorNotFound: Se o item com o ID fornecido não for encontrado.
            ErrorDelete: Se ocorrer um erro durante a exclusão.
        """
        try:
            success = self.repository.delete(id)
            if success:
                self._logger.debug(f'Item com ID {id} deletado com sucesso.')
            else:
                self._log_and_raise_warning(ErrorNotFound, f'Item com ID {id} não foi encontrado para exclusão.')
            return success
        except Exception as e:
            self._log_and_raise_error(ErrorDelete, 'Erro ao deletar item.', e)

    def _log_and_raise_warning(self, error_class, message: str, exception: Optional[Exception] = None):
        """
        Loga uma advertência e lança uma exceção correspondente.

        Args:
            error_class (Exception): Classe da exceção a ser lançada.
            message (str): Mensagem de advertência a ser logada.
            exception (Optional[Exception]): Exceção original (opcional).
        """
        self._logger.warning(message)
        raise error_class(message) from exception

    def _log_and_raise_error(self, error_class, message: str, exception: Exception):
        """
        Loga um erro e lança uma exceção correspondente.

        Args:
            error_class (Exception): Classe da exceção a ser lançada.
            message (str): Mensagem de erro a ser logada.
            exception (Exception): Exceção original que causou o erro.
        """
        error_message = f'{message}: {exception}'
        self._logger.error(error_message)
        raise error_class(error_message) from exception
    
    def count_all(self) -> int:
        """
        Conta o número total de registros.

        Returns:
            int: O número total de registros.

        Raises:
            ErrorExecution: Se ocorrer um erro durante a execução da contagem.
        """
        try:
            total_count = self.repository.count_all()
            self._logger.debug(f'Total de registros: {total_count}')
            return total_count
        except Exception as e:
            self._log_and_raise_error(ErrorExecution, 'Erro ao contar registros.', e)