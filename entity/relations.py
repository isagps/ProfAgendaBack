from config.globals import db

# Relação entre Professor e Materia (tabela de associação)
professor_materia = db.Table(
    'professor_materia',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.id'), primary_key=True),
    db.Column('materia_id', db.Integer, db.ForeignKey('materia.id'), primary_key=True)
)