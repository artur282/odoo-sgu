# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Modalidad(models.Model):
    _name = 'sgu.modalidad'
    _description = 'Modalidad de estudio (semestral, trimestral, anual)'
    _rec_name = 'modalidad'

    modalidad = fields.Char('Modalidad', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    carrera_ids = fields.One2many('sgu.carrera', 'modalidad_id', 'Carreras')
