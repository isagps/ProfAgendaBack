from entity.materia import Materia
from infrastructure.base_repository import BaseRepository

class MateriaRepository(BaseRepository[Materia]):
    """
    Repositório específico para o modelo `Materia`.

    Esta classe herda todas as funcionalidades da classe `BaseRepository` e
    está preparada para realizar operações CRUD (Create, Read, Update, Delete)
    no modelo `Materia`.

    Args:
        BaseRepository (Generic[T]): Classe base genérica para repositórios.
    """
    pass