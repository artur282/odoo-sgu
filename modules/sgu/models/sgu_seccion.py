# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Seccion(models.Model):
    _name = 'sgu.seccion'
    _description = 'Sección académica'
    _rec_name = 'codigo'

    codigo = fields.Char('Código de sección', required=True)

    # Referencias a modelos base
    carrera_id = fields.Many2one('sgu.carrera', 'Programa/Carrera', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True)
    periodo_id = fields.Many2one('sgu.periodo', 'Periodo', required=True)

    # Capacidad
    capacidad = fields.Integer('Capacidad máxima', default=40)
    capacidad_restante = fields.Integer('Cupos disponibles', compute='_compute_capacidad_restante', store=True)

    # Relaciones
    inscripcion_ids = fields.One2many('sgu.inscripcion', 'seccion_id', 'Inscripciones')
    horario_ids = fields.One2many('sgu.horario', 'seccion_id', 'Horarios')

    active = fields.Boolean('Activo', default=True)
    
    @api.depends('capacidad', 'inscripcion_ids')
    def _compute_capacidad_restante(self):
        for record in self:
            inscripciones_confirmadas = self.env['sgu.inscripcion'].search_count([
                ('seccion_id', '=', record.id),
                ('state', '=', 'confirmed')
            ])
            record.capacidad_restante = record.capacidad - inscripciones_confirmadas
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.codigo} - {record.carrera_id.name} ({record.sede_id.name})"
            result.append((record.id, name))
        return result
