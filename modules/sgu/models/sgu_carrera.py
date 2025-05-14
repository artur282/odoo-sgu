# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Carrera(models.Model):
    _name = 'sgu.carrera'
    _description = 'Programas académicos'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    codigo = fields.Char('Código', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    modalidad_id = fields.Many2one('sgu.modalidad', 'Modalidad')
    nivel_academico_id = fields.Many2one('sgu.nivel.academico', 'Nivel Académico')
    area_id = fields.Many2one('sgu.area', 'Área')
    
    # Relación One2many al modelo pivot
    carrera_sede_ids = fields.One2many('sgu.carrera.sede', 'carrera_id', string='Sedes donde se imparte')
    
    # Campo computado para obtener solo las sedes
    sede_ids = fields.Many2many('sgu.sede', string='Sedes disponibles', compute='_compute_sede_ids', store=False)
    
    def _compute_sede_ids(self):
        for carrera in self:
            carrera.sede_ids = carrera.carrera_sede_ids.mapped('sede_id')
    
    pensum_ids = fields.One2many('sgu.pensum', 'carrera_id', 'Pensums')
