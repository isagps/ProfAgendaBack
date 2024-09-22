from config.globals import db
from sqlalchemy.exc import SQLAlchemyError
import logging
import os

class DatabaseConfig:
    """
    Classe responsável pela configuração do banco de dados da aplicação Flask.

    Esta classe lida com a configuração do SQLAlchemy, a criação das tabelas do banco de dados e a
    garantia de que o diretório onde o banco de dados será salvo exista.

    Atributos da Classe:
        BASE_DIR (str): Diretório base onde o arquivo da configuração está localizado.
        DATABASE_DIR (str): Caminho completo para o diretório onde o banco de dados será armazenado.
        DATABASE_NAME (str): Nome do arquivo do banco de dados.
        DATABASE_ENGINE (str): Tipo de motor de banco de dados a ser utilizado. Padrão: 'sqlite'.

    Métodos da Classe:
        init_app(app):
            Inicializa a configuração do banco de dados, garantindo que o diretório de armazenamento
            exista e criando as tabelas do banco de dados.

        get_database_uri():
            Retorna a URI de conexão do banco de dados de acordo com o motor especificado.

        _create_tables(app):
            Cria todas as tabelas do banco de dados definidas na aplicação.

        _ensure_database_directory_exists():
            Garante que o diretório onde o banco de dados será armazenado exista. Caso não exista, o diretório será criado.
    """

    BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))  # Diretório base
    DATABASE_DIR: str = os.path.join(BASE_DIR, 'data')  # Diretório de dados
    DATABASE_NAME: str = 'database.db'  # Nome do arquivo do banco de dados
    DATABASE_ENGINE: str = 'sqlite'  # Motor de banco de dados, aqui é 'sqlite' por padrão
    
    _logger = logging.getLogger('DatabaseConfig')

    @classmethod
    def init_app(cls, app):
        """
        Inicializa o banco de dados e cria as tabelas.

        Este método deve ser chamado durante a inicialização da aplicação Flask. Ele garante
        que o diretório para o banco de dados exista e configura o SQLAlchemy para se conectar
        ao banco de dados correto.

        Parâmetros:
            app (Flask): A instância da aplicação Flask.

        Exceções:
            SQLAlchemyError: Lança exceção caso ocorra um erro durante a inicialização ou criação de tabelas.
        """
        cls._ensure_database_directory_exists()
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.get_database_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        try:
            db.init_app(app)
            cls._create_tables(app)
            cls._logger.info("Configuração do banco de dados concluída com sucesso.")
        except SQLAlchemyError as e:
            cls._logger.error(f"Erro ao inicializar o banco de dados: {e}")
            raise

    @classmethod
    def get_database_uri(cls) -> str:
        """
        Constrói e retorna a URI de conexão com o banco de dados.

        Atualmente, este método suporta apenas o motor de banco de dados SQLite, mas pode ser
        estendido para suportar outros tipos de banco de dados.

        Retorna:
            str: A URI de conexão com o banco de dados.

        Exceções:
            ValueError: Lança exceção se o motor de banco de dados não for suportado.
        """
        if cls.DATABASE_ENGINE == 'sqlite':
            return f'sqlite:///{os.path.join(cls.DATABASE_DIR, cls.DATABASE_NAME)}'
        raise ValueError(f"Motor de banco de dados '{cls.DATABASE_ENGINE}' não suportado.")

    @classmethod
    def _create_tables(cls, app):
        """
        Cria as tabelas do banco de dados dentro do contexto da aplicação Flask.

        Este método deve ser chamado após a configuração do SQLAlchemy. Ele garante que todas
        as tabelas definidas nos modelos da aplicação sejam criadas no banco de dados.

        Parâmetros:
            app (Flask): A instância da aplicação Flask.

        Exceções:
            SQLAlchemyError: Lança exceção caso ocorra um erro durante a criação das tabelas.
        """
        with app.app_context():
            try:
                db.create_all()
                cls._logger.info("Tabelas criadas com sucesso!")
            except SQLAlchemyError as e:
                cls._logger.error(f"Erro ao criar tabelas: {e}")
                raise

    @classmethod
    def _ensure_database_directory_exists(cls):
        """
        Garante que o diretório onde o banco de dados será armazenado exista.

        Se o diretório não existir, ele será criado. Isso é importante para garantir que o SQLite
        possa salvar o banco de dados no local correto.

        Exceções:
            OSError: Lança exceção caso ocorra um erro ao criar o diretório.
        """
        os.makedirs(cls.DATABASE_DIR, exist_ok=True)
        cls._logger.info(f"Diretório {cls.DATABASE_DIR} pronto para uso.")