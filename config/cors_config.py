from flask_cors import CORS
import logging

class CORSConfig:
    """
    Classe responsável por configurar o CORS (Cross-Origin Resource Sharing) na aplicação Flask.

    O CORS permite que a aplicação responda a requisições vindas de diferentes origens (domínios). 
    Isso é necessário em aplicações web que interagem com APIs hospedadas em servidores diferentes.

    Métodos:
        init_cors(app, origins="*", resources=None):
            Configura o CORS para a aplicação, permitindo que você defina as origens e os recursos que
            podem ser acessados via CORS.
    """

    @staticmethod
    def init_cors(app, origins="*", resources=None):
        """
        Inicializa e configura o CORS para a aplicação Flask.

        Args:
            app (Flask): Instância da aplicação Flask onde o CORS será configurado.
            origins (str ou list): Define quais origens têm permissão para acessar os recursos da aplicação.
                                   O valor padrão é "*" (todas as origens permitidas).
                                   Pode ser uma string ou uma lista de origens permitidas.
            resources (dict): Um dicionário que define quais caminhos de recursos podem ser acessados via CORS.
                              O valor padrão é permitir o CORS em todos os caminhos (r"/*").

        Exemplo de uso:
            CORSConfig.init_cors(app, origins=["https://example.com"], resources={r"/api/*": {"origins": "https://example.com"}})
        """
        if resources is None:
            resources = {r"/*": {"origins": origins}}
        
        CORS(app, resources=resources)
        logging.getLogger("CORSConfig").info(f"CORS configurado com origins: {origins}")