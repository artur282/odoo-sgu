from odoo import models, fields

class SguAutoridad(models.Model):
    _name = 'sgu_autoridad'
    _description = 'Autoridades de la institución'

    autoridad = fields.Many2one('sgu_tipo_autoridad', string='Tipo de autoridad', required=True)
    institucion = fields.Many2one('sgu_institucion', string='Institución', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    firmaDigital = fields.Image(string='Firma Digital', required=True)
    active = fields.Boolean(default=True, string='Estatus', required=True)
    fecha = fields.Date(string='Fecha de nombramiento', required=True)
    user_id = fields.Many2one(
        'user_registration',
        string='Usuario',
        domain=[('grupo_usuario', '=', 'autoridad')],
        required=True
    )

class SguTipoAutoridad(models.Model):
    _name = 'sgu_tipo_autoridad'
    _description = 'Tipos de autoridades de la institución'
    _rec_name = 'tipo'

    tipo = fields.Char(string='Tipo de autoridad', required=True)
    active = fields.Boolean(default=True, required=True)
