from sqlalchemy.orm import Session
from typing import Dict, Any, Set, Optional
import logging

class BaseModel:
    """
    Classe base abstrata para todas as entidades do modelo. Esta classe fornece métodos utilitários para 
    converter instâncias de modelos para e a partir de dicionários e também para representar instâncias como string.

    Atributos:
        __abstract__ (bool): Indicador de que esta é uma classe abstrata do SQLAlchemy.
        _logger (logging.Logger): Logger para registrar eventos e erros durante as operações de conversão e relacionamento.
    """
    __abstract__ = True
    _logger: logging.Logger = logging.getLogger(__name__)

    def __repr__(self) -> str:
        """
        Retorna uma representação string do objeto, listando os atributos definidos.

        Returns:
            str: Uma string que representa o objeto com seus atributos e valores.
        """
        try:
            attrs = {key: getattr(self, key) for key in self.__mapper__.attrs.keys()}
            attrs_str = ', '.join(f'{key}={value!r}' for key, value in attrs.items())
            return f'<{self.__class__.__name__}({attrs_str})>'
        except Exception as e:
            return f'<{self.__class__.__name__}(error={e})>'

    def from_dict(self, data: Dict[str, Any], session: Session) -> 'BaseModel':
        """
        Popula o objeto com os valores de um dicionário, incluindo atributos simples e relacionamentos.

        Args:
            data (Dict[str, Any]): Dicionário contendo os dados a serem aplicados ao objeto.
            session (Session): Sessão do SQLAlchemy para busca de objetos relacionados.

        Returns:
            BaseModel: A própria instância do objeto atualizada com os valores do dicionário.

        Raises:
            Exception: Se ocorrer um erro ao carregar os dados.
        """
        try:
            for key, value in data.items():
                if key in self.__mapper__.columns.keys():
                    setattr(self, key, value)
                elif key in self.__mapper__.relationships.keys():
                    self._handle_relationship(key, value, session)
                else:
                    self._logger.warning(f'Atributo {key} não encontrado na classe {self.__class__.__name__}')
            return self
        except Exception as e:
            self._logger.error(f'Erro ao carregar o objeto a partir do dicionário: {e}')
            raise

    def _handle_relationship(self, key: str, value: Any, session: Session):
        """
        Trata os relacionamentos definidos no modelo, populando os atributos relacionados de acordo
        com os dados fornecidos.

        Args:
            key (str): Nome do atributo de relacionamento.
            value (Any): Dados relacionados (pode ser um objeto ou uma lista de objetos).
            session (Session): Sessão do SQLAlchemy para buscar ou criar objetos relacionados.
        """
        rel = self.__mapper__.relationships[key]
        related_class = rel.mapper.class_

        def fetch_or_create(item):
            if 'id' in item:
                existing = session.query(related_class).get(item['id'])
                return existing.from_dict(item, session) if existing else related_class().from_dict(item, session)
            return related_class().from_dict(item, session)

        if rel.uselist:
            setattr(self, key, [fetch_or_create(item) for item in value])
        else:
            setattr(self, key, fetch_or_create(value))

    def to_dict(self, visited: Optional[Set[int]] = None, max_depth: int = 5, current_depth: int = 0) -> Optional[Dict[str, Any]]:
        """
        Converte o objeto em um dicionário, incluindo atributos simples e relacionamentos.

        Args:
            visited (Optional[Set[int]]): Conjunto de objetos já visitados para evitar loops infinitos.
            max_depth (int): Profundidade máxima de aninhamento ao serializar relacionamentos.
            current_depth (int): Profundidade atual de aninhamento.

        Returns:
            Optional[Dict[str, Any]]: Um dicionário representando o objeto ou None se a profundidade máxima for excedida.

        Raises:
            Exception: Se ocorrer um erro durante a conversão.
        """
        if visited is None:
            visited = set()
        if current_depth > max_depth or id(self) in visited:
            return self._handle_already_visited()

        visited.add(id(self))
        try:
            return self._serialize_sqlalchemy_object(visited, max_depth, current_depth) if hasattr(self, '__mapper__') else self._serialize_regular_object(visited, max_depth, current_depth)
        except Exception as e:
            self._logger.error(f'Erro ao converter o objeto para dicionário: {e}')
            raise

    def _handle_already_visited(self) -> Dict[str, Any]:
        """
        Manipula objetos já visitados para evitar loops de referência circular.

        Returns:
            Dict[str, Any]: Um dicionário com os atributos simples do objeto.
        """
        return {key: getattr(self, key, None) for key in self.__mapper__.columns.keys()}

    def _serialize_sqlalchemy_object(self, visited, max_depth, current_depth) -> Dict[str, Any]:
        """
        Serializa objetos gerenciados pelo SQLAlchemy, incluindo atributos e relacionamentos.

        Args:
            visited (Set[int]): Conjunto de objetos já visitados para evitar loops.
            max_depth (int): Profundidade máxima de aninhamento ao serializar.
            current_depth (int): Profundidade atual de aninhamento.

        Returns:
            Dict[str, Any]: Um dicionário com os dados do objeto e seus relacionamentos.
        """
        result = {key: getattr(self, key) for key in self.__mapper__.columns.keys()}
        for rel in self.__mapper__.relationships:
            value = getattr(self, rel.key)
            result[rel.key] = self._serialize_relationship(value, visited, max_depth, current_depth)
        return result

    def _serialize_relationship(self, value, visited, max_depth, current_depth):
        """
        Serializa relacionamentos, cuidando de objetos aninhados e listas de objetos.

        Args:
            value (Any): O valor do relacionamento a ser serializado.
            visited (Set[int]): Conjunto de objetos já visitados.
            max_depth (int): Profundidade máxima permitida.
            current_depth (int): Profundidade atual.

        Returns:
            Any: O relacionamento serializado ou None se a profundidade for excedida.
        """
        if value is None:
            return None
        if isinstance(value, list):
            return [item.to_dict(visited, max_depth, current_depth + 1) for item in value]
        return value.to_dict(visited, max_depth, current_depth + 1)

    def _serialize_regular_object(self, visited, max_depth, current_depth) -> Dict[str, Any]:
        """
        Serializa objetos regulares que não são gerenciados pelo SQLAlchemy.

        Args:
            visited (Set[int]): Conjunto de objetos já visitados.
            max_depth (int): Profundidade máxima permitida.
            current_depth (int): Profundidade atual.

        Returns:
            Dict[str, Any]: O dicionário com os dados do objeto.
        """
        return {key: self._serialize_value(getattr(self, key), visited, max_depth, current_depth + 1) for key in dir(self) if not key.startswith('_') and not callable(getattr(self, key))}

    def _serialize_value(self, value, visited, max_depth, current_depth):
        """
        Serializa valores individuais do objeto, incluindo listas, dicionários e valores simples.

        Args:
            value (Any): O valor a ser serializado.
            visited (Set[int]): Conjunto de objetos já visitados.
            max_depth (int): Profundidade máxima permitida.
            current_depth (int): Profundidade atual.

        Returns:
            Any: O valor serializado ou None se a profundidade for excedida.
        """
        if current_depth > max_depth:
            return None
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        if isinstance(value, list):
            return [self._serialize_value(item, visited, max_depth, current_depth + 1) for item in value]
        if isinstance(value, dict):
            return {k: self._serialize_value(v, visited, max_depth, current_depth + 1) for k, v in value.items()}
        if hasattr(value, 'to_dict'):
            return value.to_dict(visited, max_depth, current_depth + 1)
        return None