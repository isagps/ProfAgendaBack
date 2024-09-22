from config.globals import db
from infrastructure.base_entity import BaseEntity

class Horario(BaseEntity):
    """
    Representa a entidade Horario no banco de dados.

    Atributos:
        dia_da_semana (str): Dia da semana do horário (valores permitidos: SEGUNDA a DOMINGO).
        hora (str): Hora do horário (formato HH:MM).
        turma_id (int): ID da relação com a entidade Turma.
        professor_id (int): ID da relação com a entidade Professor.
        materia_id (int): ID da relação com a entidade Materia.
        turma (Turma): Relação com a entidade Turma.
        professor (Professor): Relação com a entidade Professor.
        materia (Materia): Relação com a entidade Materia.
    """
    __tablename__ = 'horario'

    dia_da_semana = db.Column(db.String(16), nullable=False)
    hora = db.Column(db.String(5), nullable=False)

    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id', ondelete='CASCADE'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)

    turma = db.relationship('Turma', back_populates='horarios')
    professor = db.relationship('Professor', back_populates='horarios')
    materia = db.relationship('Materia', back_populates='horarios')

    __table_args__ = (
        db.CheckConstraint(
            dia_da_semana.in_(['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO']), name='chk_dia_semana'
        ),
    )