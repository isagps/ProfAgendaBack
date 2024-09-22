from flask import Blueprint, request, jsonify
from infrastructure.base_model import BaseModel
from infrastructure.base_service import BaseService
from typing import Type, Dict, Any, Tuple, Generic, TypeVar
import logging

T = TypeVar('T', bound=BaseModel)

class BaseController(Generic[T]):
    """
    Classe base para controladores que implementam operações CRUD (Create, Read, Update, Delete).

    Esta classe é genérica e é utilizada para definir um conjunto de endpoints comuns, aplicados
    a um serviço específico que implementa a lógica de negócios e um modelo específico.

    Atributos:
        blueprint (Blueprint): Um blueprint do Flask, responsável por agrupar as rotas da API.
        service (BaseService[T]): Instância do serviço que lida com a lógica de negócios do modelo T.

    Métodos:
        __init__(service_class, blueprint_name, prefix):
            Inicializa o controlador com um serviço e registra as rotas associadas ao blueprint.

        register_routes():
            Registra as rotas CRUD no blueprint.

        get_by_id(id: int):
            Retorna um item baseado no ID fornecido.

        get_all():
            Retorna uma lista paginada de itens com base nos parâmetros de paginação e filtro.

        get_all_without_pagination():
            Retorna todos os itens sem paginação.

        create():
            Cria um novo item com base nos dados fornecidos no corpo da requisição.

        update(id: int):
            Atualiza um item existente com base no ID e nos dados fornecidos.

        delete(id: int):
            Deleta um item com base no ID fornecido.
    """
    
    _logger: logging.Logger

    def __init__(self, service_class: Type[BaseService[T]], blueprint_name: str, prefix: str = '/api'):
        """
        Inicializa o controlador base com um serviço e um blueprint.

        Args:
            service_class (Type[BaseService[T]]): Classe de serviço responsável por manipular o modelo de dados T.
            blueprint_name (str): Nome do blueprint Flask.
            prefix (str): Prefixo da URL para o conjunto de rotas. O padrão é '/api'.
        """
        self.blueprint: Blueprint = Blueprint(blueprint_name, __name__, url_prefix=f'{prefix}/{blueprint_name}')
        self.service: BaseService[T] = service_class()
        self.register_routes()
        self._logger = logging.getLogger(self.__class__.__name__)

    def register_routes(self) -> None:
        """
        Registra as rotas de operações CRUD no blueprint.

        As seguintes rotas são registradas:
        - GET /<int:id>: Busca um item pelo ID.
        - GET /: Retorna uma lista paginada de itens.
        - GET /all: Retorna todos os itens sem paginação.
        - GET /count: Conta o número total de registros.
        - POST /: Cria um novo item.
        - PUT /<int:id>: Atualiza um item existente.
        - DELETE /<int:id>: Deleta um item existente.
        """
        routes = [
            ('/<int:id>', 'get_by_id', self.get_by_id, ['GET']),
            ('/', 'get_all', self.get_all, ['GET']),
            ('/all', 'get_all_without_pagination', self.get_all_without_pagination, ['GET']),
            ('/count', 'count_all', self.count_all, ['GET']),
            ('/', 'create', self.create, ['POST']),
            ('/<int:id>', 'update', self.update, ['PUT']),
            ('/<int:id>', 'delete', self.delete, ['DELETE'])
        ]
        for route, endpoint, view_func, methods in routes:
            self.blueprint.add_url_rule(route, endpoint, view_func, methods=methods)

    def get_by_id(self, id: int) -> Tuple[Dict[str, Any], int]:
        """
        Busca um item pelo ID.

        Args:
            id (int): O ID do item a ser buscado.

        Retorna:
            Tuple[Dict[str, Any], int]: O item no formato JSON e o status HTTP 200.
        """
        self._logger.info(f'Obtendo item com ID {id}')
        result = self.service.get_by_id(id)
        return jsonify(result.to_dict()), 200

    def get_all(self) -> Tuple[Dict[str, Any], int]:
        """
        Busca uma lista paginada de itens, com base nos parâmetros de paginação e filtro.

        Retorna:
            Tuple[Dict[str, Any], int]: Lista paginada de itens no formato JSON e o status HTTP 200.
        """
        page_number = int(request.args.get('page_number', 1))
        page_size = int(request.args.get('page_size', 10))
        filter_str = request.args.get('filter', '')
        
        self._logger.info(f'Obtendo itens - Página {page_number}, Tamanho {page_size}, Filtro "{filter_str}"')
        results = self.service.get_all(page_number, page_size, filter_str)
        return jsonify(results.to_dict()), 200

    def get_all_without_pagination(self) -> Tuple[Dict[str, Any], int]:
        """
        Busca todos os itens sem paginação.

        Retorna:
            Tuple[Dict[str, Any], int]: Lista de todos os itens no formato JSON e o status HTTP 200.
        """
        self._logger.info('Obtendo todos os itens sem paginação')
        results = self.service.get_all_without_pagination()
        return jsonify([item.to_dict() for item in results]), 200

    def create(self) -> Tuple[Dict[str, Any], int]:
        """
        Cria um novo item com base nos dados fornecidos.

        Retorna:
            Tuple[Dict[str, Any], int]: O item criado no formato JSON e o status HTTP 201.
        """
        data = request.json
        self._logger.info(f'Criando novo item com dados: {data}')
        result = self.service.create(data)
        return jsonify(result.to_dict()), 201

    def update(self, id: int) -> Tuple[Dict[str, Any], int]:
        """
        Atualiza um item existente com base no ID e nos dados fornecidos.

        Args:
            id (int): O ID do item a ser atualizado.

        Retorna:
            Tuple[Dict[str, Any], int]: O item atualizado no formato JSON e o status HTTP 200.
        """
        data = request.json
        self._logger.info(f'Atualizando item com ID {id} com dados: {data}')
        result = self.service.update(id, data)
        return jsonify(result.to_dict()), 200

    def delete(self, id: int) -> Tuple[Dict[str, Any], int]:
        """
        Deleta um item existente com base no ID fornecido.

        Args:
            id (int): O ID do item a ser deletado.

        Retorna:
            Tuple[Dict[str, Any], int]: Mensagem de sucesso e o status HTTP 204.
        """
        self._logger.info(f'Deletando item com ID {id}')
        self.service.delete(id)
        return jsonify({'mensagem': 'Deletado com sucesso'}), 204
    
    def count_all(self) -> Tuple[Dict[str, Any], int]:
        """
        Conta o número total de registros.

        Retorna:
            Tuple[Dict[str, Any], int]: O número total de registros no formato JSON e o status HTTP 200.
        """
        self._logger.info('Contando o total de registros')
        total_count = self.service.count_all()
        return jsonify({'total_count': total_count}), 200