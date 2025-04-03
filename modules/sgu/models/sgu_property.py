from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SguAutoridad(models.Model):
    _name = 'sgu_autoridad'
    _description = 'Autoridades de la institución'

    autoridad = fields.Many2one('sgu_tipo_autoridad', string='Tipo de autoridad', required=True)
    institucion = fields.Many2one('sgu_institucion', string='Institución', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    firmaDigital = fields.Image(string='Firma Digital', required=True)
    active = fields.Boolean(default=True, string='Estatus', required=True)
    fecha = fields.Date(string='Fecha de nombramiento', required=True)
    


class SguTipoAutoridad(models.Model):
    _name = 'sgu_tipo_autoridad'
    _description = 'Tipos de autoridades de la institución'
    _rec_name = 'tipo'

    tipo = fields.Char(string='Tipo de autoridad', required=True)
    active = fields.Boolean(default=True, required=True)


class SguCarreras(models.Model):
    _name = 'sgu_carreras'
    _description = 'Carreras del instituto'
    _rec_name = 'carrera'

    codigo = fields.Integer(string='Código', required=True)
    carrera = fields.Char(string='Carrera', required=True)
    modalidad_carrera = fields.Many2one('sgu_modalidad', string='Modalidad', required=True)
    active = fields.Boolean(default=True, required=True)
    area_carrea = fields.Many2one('sgu_areas', string='Area', required=True)
    nivel_academico = fields.Many2one('sgu_nivel_academico', string='Nivel académico', required=True)
    sede = fields.Many2one('sgu_sedes', string='Sede', required=True)
    active = fields.Boolean(string="Activo", default=True)
    pensum = fields.Many2one('university.pensum', string='Pensum', required=True)


class SguAreas(models.Model):
    _name = 'sgu_areas'
    _description = 'areas de la instucion'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    codigo= fields.Integer(string='Codigo', required=True)
    carrera_area = fields.One2many('sgu_carreras', 'area_carrea', string='Carreras')
    
    active = fields.Boolean(string="Activo", default=True)
    
class SguModalidad(models.Model):
    _name = 'sgu_modalidad'
    _description = 'Modalidades de la institución'
    _rec_name = 'modalidad'

    modalidad = fields.Char(string='Modalidad', required=True)
    active = fields.Boolean(default=True, required=True)

class SguNivelAcademico(models.Model):
    _name = 'sgu_nivel_academico'
    _description = 'Niveles académicos de la institución'
    _rec_name = 'nivel'

    nivel = fields.Char(string='Nivel académico', required=True)
    active = fields.Boolean(default=True, required=True)