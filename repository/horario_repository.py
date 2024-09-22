from entity.horario import Horario
from infrastructure.base_repository import BaseRepository

class HorarioRepository(BaseRepository[Horario]):
    """
    Repositório específico para o modelo `Horario`.

    Esta classe herda todas as funcionalidades da classe `BaseRepository` e
    está preparada para realizar operações CRUD (Create, Read, Update, Delete)
    no modelo `Horario`.

    Args:
        BaseRepository (Generic[T]): Classe base genérica para repositórios.
    """
    pass