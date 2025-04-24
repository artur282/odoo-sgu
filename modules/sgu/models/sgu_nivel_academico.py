from odoo import models, fields

class SguNivelAcademico(models.Model):
    _name = 'sgu_nivel_academico'
    _description = 'Niveles académicos de la institución'
    _rec_name = 'nivel'

    nivel = fields.Char(string='Nivel académico', required=True)
    active = fields.Boolean(default=True, required=True)
