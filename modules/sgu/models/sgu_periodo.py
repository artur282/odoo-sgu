# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Periodo(models.Model):
    _name = 'sgu.periodo'
    _description = 'Periodo académico'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)  # Ej: 2025-1
    anio = fields.Integer('Año', required=True)
    periodo = fields.Selection([
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV')
    ], string='Periodo', required=True)
    modalidad = fields.Selection([
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual')
    ], string='Modalidad', required=True)
    fecha_inicio = fields.Date('Fecha inicio', required=True)
    fecha_fin = fields.Date('Fecha fin', required=True)
    active = fields.Boolean('Activo', default=True)
    descripcion = fields.Text('Descripción')

    # Relaciones
    proceso_ids = fields.One2many('sgu.proceso', 'periodo_id', 'Procesos')
    
    @api.onchange('anio', 'periodo')
    def _onchange_anio_periodo(self):
        if self.anio and self.periodo:
            self.name = f"{self.anio}-{self.periodo}"
