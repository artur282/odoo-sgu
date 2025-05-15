# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Institucion(models.Model):
    _inherit = 'res.company'
    _description = 'Institución Universitaria (extiende res.company)'

    
    codigo = fields.Char('Código', required=True)
    descripcion = fields.Html(string='Descripción')

    
    # name: Ya está en res.company
    # direccion: Sustituido por los campos de dirección de res.company (street, city, etc.)
    # telefono: Sustituido por el campo 'phone' de res.company
    # email: Sustituido por el campo 'email' de res.company
    # logo: Sustituido por los campos de imagen de res.company (image_1920, etc.)
    # active: Ya está en res.company

    # --- Relación---
    sede_ids = fields.One2many('sgu.sede', 'institucion_id', 'Sedes')