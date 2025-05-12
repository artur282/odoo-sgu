# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Area(models.Model):
    _name = 'sgu.area'
    _description = 'Áreas de la institución'
    _rec_name = 'name'

    name = fields.Char('Nombre del área', required=True)
    codigo = fields.Char('Código', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)
    telefono = fields.Char('Teléfono')
    
    # Relaciones
    carrera_ids = fields.One2many('sgu.carrera', 'area_id', 'Carreras')
