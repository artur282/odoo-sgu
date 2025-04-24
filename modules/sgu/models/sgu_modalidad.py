from odoo import models, fields

class SguModalidad(models.Model):
    _name = 'sgu_modalidad'
    _description = 'Modalidades de la institución'
    _rec_name = 'modalidad'

    modalidad = fields.Char(string='Modalidad', required=True)
    active = fields.Boolean(default=True, required=True)
