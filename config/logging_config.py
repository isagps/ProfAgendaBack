from logging.handlers import RotatingFileHandler
import logging

class BaseLoggingConfig:
    """
    Classe base para configuração de logging.
    """
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL: int = logging.DEBUG

    @classmethod
    def configure_logger(cls, handler: logging.Handler, level: int = None):
        """
        Configura um handler para o logger global com o formato e nível especificados.

        Args:
            handler (logging.Handler): O handler que será adicionado ao logger.
            level (int, optional): O nível de logging a ser configurado. Usa LOG_LEVEL por padrão.
        """
        formatter = logging.Formatter(cls.LOG_FORMAT)
        handler.setFormatter(formatter)
        handler.setLevel(level or cls.LOG_LEVEL)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(cls.LOG_LEVEL)


class ConsoleLoggingConfig(BaseLoggingConfig):
    """
    Configuração de logging para o console.
    """
    @classmethod
    def setup_console_logging(cls):
        """Configura logging para o console."""
        console_handler = logging.StreamHandler()
        cls.configure_logger(console_handler)
        logging.getLogger('ConsoleLoggingConfig').info("Console logging configurado")


class FileLoggingConfig(BaseLoggingConfig):
    """
    Configuração de logging para arquivo com rotação de arquivos.
    """
    LOG_FILE_NAME: str = 'app.log'
    LOG_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    LOG_FILE_BACKUP: int = 5

    @classmethod
    def setup_file_logging(cls):
        """Configura logging rotativo para arquivo."""
        file_handler = RotatingFileHandler(cls.LOG_FILE_NAME, maxBytes=cls.LOG_FILE_SIZE, backupCount=cls.LOG_FILE_BACKUP)
        cls.configure_logger(file_handler, level=logging.INFO)
        logging.getLogger('FileLoggingConfig').info("File logging configurado")