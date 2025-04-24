from odoo import models, fields

class SguAsignarCarreraSede(models.Model):
    _name = 'sgu_asignar_carrera_sede'
    _description = 'Asignar Carreras a Sedes'

    sede_id = fields.Many2one('sgu_sedes', string='Sede', required=True)
    carrera_id = fields.Many2many('sgu_carreras', string='Carreras', required=True)
    active = fields.Boolean(string='Activo', default=True)

    _sql_constraints = [
        ('unique_sede_carrera', 'unique(sede_id)', 'Cada sede debe tener una lista única de carreras.')
    ]
