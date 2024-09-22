from config.cors_config import CORSConfig
from config.database_config import DatabaseConfig
from config.logging_config import ConsoleLoggingConfig, FileLoggingConfig
from controller import register_blueprints
from exception.handlers import ErrorHandlerRegistry
from flask import Flask
import logging

def create_app(debug=False) -> Flask:
    """Cria e configura a instância da aplicação Flask."""
    app = Flask(__name__)
    app.debug = debug  # Definindo o modo de depuração da aplicação
    
    # Configuração de logging
    ConsoleLoggingConfig.setup_console_logging()
    if not app.debug:
        FileLoggingConfig.setup_file_logging()
    
    # Inicialização do banco de dados e CORS
    DatabaseConfig.init_app(app)
    CORSConfig.init_cors(app)
    
    # Registro de handlers de exceção e rotas
    ErrorHandlerRegistry(app)
    register_blueprints(app)

    logging.getLogger('app').info("Configuração da aplicação concluída")
    return app

if __name__ == '__main__':
    app = create_app(debug=False)
    app.run()