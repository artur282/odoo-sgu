# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Proceso(models.Model):
    _name = 'sgu.proceso'
    _description = 'Proceso académico'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    tipo = fields.Selection([
        ('inscripcion', 'Inscripción'),
        ('carga_horario', 'Carga de Horarios'),
        ('carga_notas', 'Carga de Notas'),
        ('retiro', 'Retiro de materias')
    ], string='Tipo', required=True)
    periodo_id = fields.Many2one('sgu.periodo', 'Periodo', required=True)
    fecha_inicio = fields.Date('Fecha inicio', required=True)
    fecha_fin = fields.Date('Fecha fin', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('closed', 'Cerrado')
    ], string='Estado', default='draft')
    descripcion = fields.Text('Descripción')

    # Campos específicos por tipo
    carrera_ids = fields.Many2many('sgu.carrera', string='Carreras aplicables')
    
    def action_activate(self):
        """Activar el proceso"""
        for record in self:
            record.state = 'active'
    
    def action_close(self):
        """Cerrar el proceso"""
        for record in self:
            record.state = 'closed'
