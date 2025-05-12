# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PensumSubject(models.Model):
    _name = 'sgu.pensum.subject'
    _description = 'Materia del pensum'
    _rec_name = 'name'

    pensum_id = fields.Many2one('sgu.pensum', 'Pensum', required=True)
    code = fields.Char('Código', required=True)
    name = fields.Char('Nombre', required=True)
    semester = fields.Integer('Semestre')
    uc = fields.Integer('Unidades de Crédito')
    prelaciones = fields.Char('Prelaciones')
    
    # Campos adicionales que podrían ser útiles
    horas_teoricas = fields.Integer('Horas Teóricas', default=0)
    horas_practicas = fields.Integer('Horas Prácticas', default=0)
    horas_totales = fields.Integer('Horas Totales', compute='_compute_horas_totales', store=True)
    
    @api.depends('horas_teoricas', 'horas_practicas')
    def _compute_horas_totales(self):
        for record in self:
            record.horas_totales = record.horas_teoricas + record.horas_practicas
