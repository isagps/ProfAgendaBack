# ProfAgenda

**ProfAgenda** é uma API desenvolvida em Flask para auxiliar na gestão dos horários dos professores da Escola Estadual Jorge Duprat Figueiredo, localizada na zona leste de São Paulo, no bairro Jardim Santa Terezinha. O objetivo deste trabalho é otimizar a gestão de tempo e organização das atividades escolares, facilitando a criação, atualização, listagem e exclusão de compromissos, além de gerenciar os horários de trabalho de professores e turmas.

Este projeto faz parte de um **Trabalho de Extensão de Curso** apresentado à **Universidade Estácio de Sá de São Paulo**, como parte dos requisitos para obtenção do título de **Tecnólogo em Análise e Desenvolvimento de Sistemas**.

**Orientador**: Prof. Me. Robson Lorbieski

## Contexto Social

O trabalho visa beneficiar a comunidade do Jardim Santa Terezinha, na zona leste de São Paulo, oferecendo uma ferramenta que melhora a gestão das atividades escolares e, consequentemente, o desempenho e bem-estar dos professores, alunos e gestores da escola.

## Arquitetura do Projeto

O projeto segue uma arquitetura **cliente-servidor**, sendo que:

- **Backend**: Desenvolvido em **Python** utilizando o framework **Flask**. O backend fornece uma API REST que gerencia todas as operações relacionadas aos horários e compromissos dos professores.
- **Frontend**: Desenvolvido em **TypeScript** utilizando **Angular**. O frontend oferece uma interface amigável e intuitiva para os usuários interagirem com o sistema.

## Requisitos

Antes de começar, certifique-se de que seu ambiente atenda aos seguintes requisitos:

- Python 3.10.11+
- pip (gerenciador de pacotes do Python)

## Frontend do Projeto

O frontend deste projeto foi desenvolvido separadamente e pode ser acessado através do seguinte repositório:

- [Frontend ProfAgenda](https://github.com/isagps/ProfAgendaFront)

## Instruções de Instalação

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### 1. Clonando o Repositório

Clone o repositório do projeto e navegue até o diretório do backend:

```bash
git clone https://github.com/isagps/ProfAgendaBack.git
```

### 2. Criando e Ativando o Ambiente Virtual

É recomendado usar um ambiente virtual para isolar as dependências do projeto. Para criar e ativar o ambiente virtual, use os comandos abaixo:

**No Windows**:

```bash
python -m venv .venv
.venv\Scripts\activate
```

**No Linux/macOS**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalando as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Se não houver um arquivo `requirements.txt`, você pode instalar manualmente:

```bash
pip install flask Flask-CORS flask_sqlalchemy
```

### 4. Configuração do Banco de Dados

A configuração do banco de dados é feita no arquivo `config/database_config.py`. O projeto utiliza SQLAlchemy para integrar com o banco de dados. O caminho do banco de dados e o tipo de motor de banco de dados são definidos de acordo com as variáveis da classe `DatabaseConfig`. A configuração para o SQLite, por exemplo, segue o padrão:

```python
BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))  # Diretório base
DATABASE_DIR: str = os.path.join(BASE_DIR, 'data')  # Diretório onde o banco de dados será salvo
DATABASE_NAME: str = 'database.db'  # Nome do arquivo de banco de dados
DATABASE_ENGINE: str = 'sqlite'  # Motor de banco de dados, aqui definido como 'sqlite'
```

Essa configuração garante que o banco de dados SQLite será armazenado no diretório `config/data/database.db`.

### 5. Executando o Projeto

Após a configuração do banco de dados e a instalação das dependências, execute o servidor Flask:

```bash
python app.py
```

O servidor estará disponível em:

```
http://127.0.0.1:5000
```

## Estrutura do Projeto

Aqui está uma visão geral da estrutura do projeto:

<details>
  <summary><strong>Estrutura do Projeto</strong></summary>
  <pre>
profAgenda/
│
├── back/
│   ├── app.py                                # Arquivo principal da aplicação
│   ├── app.log                               # Arquivo de log da aplicação
│   ├── requirements.txt                      # Dependências do projeto
│   ├── config/                               # Configurações
│   │   ├── cors_config.py                    # Configuração de CORS
│   │   ├── database_config.py                # Configuração do banco de dados
│   │   ├── globals.py                        # Variáveis globais (ex.: instância do db)
│   │   ├── logging_config.py                 # Configuração de logging
│   │   └── data/
│   │       └── database.db                   # Arquivo de banco de dados SQLite
│   ├── controller/                           # Controladores
│   │   ├── horario_controller.py
│   │   ├── materia_controller.py
│   │   ├── professor_controller.py
│   │   └── turma_controller.py
│   ├── entity/                               # Entidades do modelo de dados
│   │   ├── horario.py
│   │   ├── materia.py
│   │   ├── professor.py
│   │   ├── turma.py
│   │   └── relations.py                      # Definição das relações entre as entidades
│   ├── exception/                            # Tratamento de exceções
│   │   ├── error_creation.py
│   │   ├── error_delete.py
│   │   ├── error_execution.py
│   │   ├── error_invalid_object.py
│   │   ├── error_not_found.py
│   │   ├── error_object_already_exists.py
│   │   └── error_update.py
│   ├── infrastructure/                       # Infraestrutura
│   │   ├── base_controller.py
│   │   ├── base_entity.py
│   │   ├── base_error.py
│   │   ├── base_model.py
│   │   ├── base_repository.py
│   │   └── base_service.py
│   ├── model/                                # Modelos
│   │   └── page.py                           # Modelo para paginação
│   ├── repository/                           # Repositórios de dados
│   │   ├── horario_repository.py
│   │   ├── materia_repository.py
│   │   ├── professor_repository.py
│   │   └── turma_repository.py
│   ├── service/                              # Serviços de negócio
│   │   ├── horario_service.py
│   │   ├── materia_service.py
│   │   ├── professor_service.py
│   │   └── turma_service.py
└── README.md                                 # Manual de instalação e informações
  </pre>
</details>

## Dependências do Projeto

As principais dependências do projeto incluem:

- [Flask](https://flask.palletsprojects.com/) - Framework web minimalista.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) - Extensão para habilitar CORS nas rotas.
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Extensão para trabalhar com SQLAlchemy.

## Autor

- **Isabel Gomes Prado da Silva** - Desenvolvedora