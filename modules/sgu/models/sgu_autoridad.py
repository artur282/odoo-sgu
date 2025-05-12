# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Autoridad(models.Model):
    _name = 'sgu.autoridad'
    _description = 'Autoridad universitaria'
    _rec_name = 'name'

    name = fields.Char('Nombre completo', required=True)
    cargo = fields.Char('Cargo', required=True)
    firma = fields.Binary('Firma digital')
    email = fields.Char('Correo electrónico')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    sede_id = fields.Many2one('sgu.sede', 'Sede asignada')
    
    # Campos adicionales útiles
    fecha_inicio_cargo = fields.Date('Fecha inicio del cargo')
    fecha_fin_cargo = fields.Date('Fecha fin del cargo')
    telefono = fields.Char('Teléfono')
    puede_firmar_documentos = fields.Boolean('Puede firmar documentos', default=True)
