# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Pensum(models.Model):
    _name = 'sgu.pensum'
    _description = 'Pensum universitario'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    carrera_id = fields.Many2one('sgu.carrera', 'Carrera', required=True)
    fecha_aprobacion = fields.Date('Fecha de aprobación')
    vigente = fields.Boolean('Vigente', default=True)

    # Relaciones
    subject_ids = fields.One2many('sgu.pensum.subject', 'pensum_id', 'Materias')
    
    def toggle_vigencia(self):
        """Toggle the vigencia status"""
        for record in self:
            record.vigente = not record.vigente
