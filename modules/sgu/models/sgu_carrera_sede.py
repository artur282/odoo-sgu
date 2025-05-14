# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CarreraSede(models.Model):
    _name = 'sgu.carrera.sede'
    _description = 'Relación entre Carreras y Sedes'
    _rec_name = 'display_name'

    # Campos relacionales
    carrera_id = fields.Many2one('sgu.carrera', 'Carrera', required=True, ondelete='cascade')
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True, ondelete='cascade')
    
    # Campos computados
    display_name = fields.Char('Nombre', compute='_compute_display_name', store=True)
    
    # Campos adicionales que se pueden agregar a la relación
    active = fields.Boolean('Activo', default=True)
    observaciones = fields.Text('Observaciones')
    
    @api.depends('carrera_id.name', 'sede_id.name')
    def _compute_display_name(self):
        for record in self:
            if record.carrera_id and record.sede_id:
                record.display_name = f"{record.carrera_id.name}-{record.sede_id.name}"
            else:
                record.display_name = False
    
    # Restricción SQL para garantizar la unicidad de la combinación (carrera_id, sede_id)
    _sql_constraints = [
        ('carrera_sede_unique', 'unique(carrera_id, sede_id)', 
         'Esta carrera ya está asignada a esta sede')
    ]
    
    # Relaciones adicionales al modelo pivot
    # Nota: Para usar estas relaciones, los modelos sgu.proceso y sgu.horario
    # deben tener un campo Many2one que apunte a este modelo, por ejemplo:
    # carrera_sede_id = fields.Many2one('sgu.carrera.sede', 'Carrera en Sede')
    
    # Como referencia para futuras implementaciones:
    # proceso_ids = fields.One2many('sgu.proceso', 'carrera_sede_id', 'Procesos')
    # horario_ids = fields.One2many('sgu.horario', 'carrera_sede_id', 'Horarios')
