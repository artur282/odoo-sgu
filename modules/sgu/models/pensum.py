# models/pensum.py
from odoo import models, fields, api

class UniversityPensum(models.Model):
    _name = 'university.pensum'
    _description = 'Pensum Universitario'

    name = fields.Char(
        string='Nombre del Pensum',
        required=True
    )
    subject_ids = fields.One2many(
        'university.pensum.subject',
        'pensum_id',
        string='Materias'
    )

class UniversityPensumSubject(models.Model):
    _name = 'university.pensum.subject'
    _description = 'Materias del Pensum'

    semester = fields.Char(string='Semestre')
    code = fields.Char(string='Código')
    name = fields.Char(string='Asignatura')
    uc = fields.Integer(string='U.C.')
    prelaciones = fields.Char(string='Prelaciones')

    pensum_id = fields.Many2one(
        'university.pensum',
        string='Pensum',
        ondelete='cascade'
    )
