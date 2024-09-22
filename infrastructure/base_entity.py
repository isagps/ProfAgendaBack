from config.globals import db
from infrastructure.base_model import BaseModel

class BaseEntity(db.Model, BaseModel):
    """
    Classe base abstrata para todas as entidades do banco de dados.

    Esta classe combina a funcionalidade do SQLAlchemy (`db.Model`) com a classe `BaseModel`,
    que fornece métodos adicionais, como serialização e deserialização. Atributos comuns, como `id`,
    são definidos aqui para serem herdados por outras entidades.

    Atributos:
        id (int): Chave primária da entidade, gerada automaticamente com auto-incremento.
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)