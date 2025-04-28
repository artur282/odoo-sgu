from odoo import models, fields

class SguCarreras(models.Model):
    _name = 'sgu_carreras'
    _description = 'Carreras del instituto'
    _rec_name = 'carrera'

    codigo = fields.Integer(string='Código', required=True)
    carrera = fields.Char(string='Carrera', required=True)
    modalidad_carrera = fields.Many2one('sgu_modalidad', string='Modalidad', required=True)
    active = fields.Boolean(default=True)
    area_carrera = fields.Many2one('sgu_areas', string='Área', required=True)
    nivel_academico = fields.Many2one('sgu_nivel_academico', string='Nivel académico', required=True)
    pensum = fields.Many2one('university.pensum', string='Pensum')
