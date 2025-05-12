# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Horario(models.Model):
    _name = 'sgu.horario'
    _description = 'Horario académico'
    _rec_name = 'seccion_id'

    seccion_id = fields.Many2one('sgu.seccion', 'Sección', required=True)
    asignatura = fields.Char('Asignatura', required=True)
    profesor = fields.Char('Profesor', required=True)
    aula = fields.Char('Aula')

    dia_semana = fields.Selection([
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('7', 'Domingo')
    ], string='Día', required=True)

    hora_inicio = fields.Float('Hora inicio', required=True)
    hora_fin = fields.Float('Hora fin', required=True)
    duracion = fields.Float('Duración', compute='_compute_duracion', store=True)

    active = fields.Boolean('Activo', default=True)
    
    @api.depends('hora_inicio', 'hora_fin')
    def _compute_duracion(self):
        for record in self:
            record.duracion = record.hora_fin - record.hora_inicio if record.hora_fin > record.hora_inicio else 0
            
    @api.onchange('hora_inicio', 'hora_fin')
    def _onchange_horas(self):
        if self.hora_inicio and self.hora_fin and self.hora_fin <= self.hora_inicio:
            return {'warning': {
                'title': 'Advertencia',
                'message': 'La hora de fin debe ser posterior a la hora de inicio.'
            }}
