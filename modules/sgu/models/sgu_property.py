from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SguAutoridad(models.Model):
    _name = 'sgu_autoridad'
    _description = 'Autoridades de la institución'

    autoridad = fields.Many2one('sgu_tipo_autoridad', string='Tipo de autoridad', required=True)
    institucion = fields.Many2one('sgu_instituto', string='Institución', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    firmaDigital = fields.Image(string='Firma Digital', required=True)
    active = fields.Boolean(default=True, string='Estatus', required=True)
    fecha = fields.Date(string='Fecha de nombramiento', required=True, defafault=fields.Date.today())


class SguTipoAutoridad(models.Model):
    _name = 'sgu_tipo_autoridad'
    _description = 'Tipos de autoridades de la institución'
    _rec_name = 'tipo'

    tipo = fields.Char(string='Tipo de autoridad', required=True)
    active = fields.Boolean(default=True, required=True)


class SguCarreras(models.Model):
    _name = 'sgu_carreras'
    _description = 'Carreras de la instituto'
    _rec_name = 'carrera'

    codigo = fields.Integer(string='Código', required=True)
    carrera = fields.Char(string='Carrera', required=True)
    modalidad = fields.Selection([
        ('anual', 'Anual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral')
    ], string='Modalidad', required=True)
    active = fields.Boolean(default=True, required=True)


class SguInstituto(models.Model):
    _name = 'sgu_instituto'
    _description = 'Institutos de la universidad'  
    _rec_name = 'nombre' 

    codigo_opsu = fields.Integer(string='Código OPSU', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción', required=True)
    direccion = fields.Char(string='Dirección', required=True)
    telefono = fields.Char(string='Teléfono', required=True)
    correo = fields.Char(string='Correo', required=True)
    active = fields.Boolean(default=True, required=True)

class SguAreas(models.Model):
    _name = 'sgu_areas'
    _description = 'areas de la instucion'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    codigo= fields.Integer(string='Codigo', required=True)
    carrera = fields.Many2one('sgu_carreras', string='Carrera', required=True)