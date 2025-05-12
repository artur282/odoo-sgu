# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CarreraSede(models.Model):
    _name = 'sgu.carrera.sede'
    _description = 'Asignación carreras a sedes'
    _rec_name = 'sede_id'

    carrera_ids = fields.Many2many('sgu.carrera', string='Carreras', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True)
    activo = fields.Boolean('Activo', default=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], string='Estado', default='draft')
    
    # Restricción de unicidad por sede
    _sql_constraints = [
        ('sede_unique', 'unique(sede_id)', 
         'Esta sede ya tiene asignadas carreras. Edite el registro existente.')
    ]
    
    def action_activate(self):
        """Activar la relación carrera-sede"""
        for record in self:
            record.state = 'active'
    
    def action_inactivate(self):
        """Inactivar la relación carrera-sede"""
        for record in self:
            record.state = 'inactive'
