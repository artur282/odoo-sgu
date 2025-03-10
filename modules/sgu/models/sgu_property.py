from odoo import models, fields

class SguAutoridad(models.Model):
    _name = 'sgu_autoridad'
    _description = 'Autoridades de la institución'

    autoridad = fields.Many2one('sgu_tipo_autoridad', string='Tipo de autoridad')
    institucion = fields.Many2one('sgu_instituto', string='Institución')
    nombre = fields.Char(string='Nombre')
    firmaDigital = fields.Image(string='Firma Digital')
    active = fields.Boolean(default=True ,string='Estatus')

class SguTipoAutoridad(models.Model):
    _name = 'sgu_tipo_autoridad'
    _description = 'Tipos de autoridades de la institución'
    _rec_name = 'tipo'

    tipo = fields.Char(string='Tipo de autoridad')
    active = fields.Boolean(default=True)

class SguCarreras(models.Model):
    _name = 'sgu_carreras'
    _description = 'Carreras de la instituto'

    codigo = fields.Integer(string='Código')
    carrera = fields.Char(string='Carrera')
    modalidad = fields.Selection([
        ('anual', 'Anual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral')
    ], string='Modalidad')
    active = fields.Boolean(default=True)

class SguInstituto(models.Model):
    _name = 'sgu_instituto'
    _description = 'Institutos de la universidad'  
    _rec_name = 'nombre' 

    codigo_opsu = fields.Integer(string='Código OPSU')
    nombre = fields.Char(string='Nombre')
    descripcion = fields.Text(string='Descripción')
    direccion = fields.Char(string='Dirección')
    telefono = fields.Integer(string='Teléfono')
    correo = fields.Char(string='Correo')
    active = fields.Boolean(default=True)

