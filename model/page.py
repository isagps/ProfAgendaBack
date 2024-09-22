from infrastructure.base_model import BaseModel
from typing import Generic, List, TypeVar

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    """
    Classe que representa uma página de resultados paginados.

    Esta classe armazena uma lista de itens paginados e informações de paginação, 
    como o número da página, o tamanho da página e o total de itens.

    Atributos:
        items (List[T]): A lista de itens na página atual.
        page_number (int): O número da página atual.
        page_size (int): O número de itens por página.
        total_items (int): O número total de itens disponíveis.
    """
    
    def __init__(self, items: List[T], page_number: int, page_size: int, total_items: int):
        """
        Inicializa a classe Page com os itens paginados e os detalhes de paginação.

        Args:
            items (List[T]): A lista de itens a serem exibidos nesta página.
            page_number (int): O número da página atual.
            page_size (int): O número de itens por página.
            total_items (int): O número total de itens disponíveis para paginação.
        """
        self.items = items
        self.page_number = page_number
        self.page_size = page_size
        self.total_items = total_items