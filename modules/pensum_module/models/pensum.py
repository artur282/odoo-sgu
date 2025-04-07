from odoo import models, fields

class PensumRecord(models.Model):
    _name = 'pensum.record'
    _description = 'Registro del Pensum'

    semestre = fields.Selection([
        ('1', 'Semestre 1'),
        ('2', 'Semestre 2'),
        ('3', 'Semestre 3'),
        ('4', 'Semestre 4'),
        ('5', 'Semestre 5'),
    ], string='Semestre', required=True)
    codigo = fields.Char(string='Código', required=True)
    asignatura = fields.Char(string='Asignatura', required=True)
    uc = fields.Integer(string='U.C', required=True)
    prelacion = fields.Char(string='Prelaciones', required=True)
