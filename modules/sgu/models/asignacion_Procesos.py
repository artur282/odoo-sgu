from odoo import models, fields

class AsignacionProcesoCarrera(models.Model):
    _name = 'prueba1.asignacionprocesocarrera'
    _description = 'Asignación de Proceso a Periodo Académico y Carrera'

    periodo_id = fields.Many2one('prueba1.periodoa', string='Periodo Académico', required=True)
    carrera_id = fields.Many2one('sgu_carreras', string='Carrera', required=True)
    proceso_id = fields.Many2one('prueba1.procesos', string='Proceso', required=True)

    _sql_constraints = [
        ('unique_periodo_carrera_proceso',
         'unique(periodo_id, carrera_id, proceso_id)',
         'Ya existe este proceso asignado a esta carrera y periodo académico.'),
    ]