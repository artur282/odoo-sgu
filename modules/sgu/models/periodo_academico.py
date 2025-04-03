from odoo import models, fields

class PeriodoAcademico(models.Model):
    _name = 'periodo_academico'
    _description = 'Periodo Académico'

    ano = fields.Char(string='Año', required=True)
    active = fields.Boolean(string="estatus", default=True)