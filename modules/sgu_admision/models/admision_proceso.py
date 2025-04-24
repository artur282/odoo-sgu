# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class AdmisionProceso(models.Model):
    _name = 'admision.proceso'
    _description = 'Proceso de Admisión'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc'

    name = fields.Char('Nombre', required=True, tracking=True)
    tipo = fields.Selection([
        ('preinscripcion', 'Preinscripción'),
        ('carga_horarios', 'Carga de Horarios'),
        ('inscripcion', 'Inscripción')
    ], string='Tipo de Proceso', required=True, tracking=True)
    
    periodo_id = fields.Many2one('admision.periodo', string='Periodo Académico', required=True, tracking=True)
    fecha_inicio = fields.Date('Fecha de Inicio', required=True, tracking=True)
    fecha_fin = fields.Date('Fecha de Cierre', required=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('closed', 'Cerrado')
    ], string='Estado', default='draft', tracking=True)
    
    programa_ids = fields.Many2many('admision.programa', string='Programas Disponibles')
    
    # Campos para cupos cuando el proceso es de preinscripción
    cupos_opsu = fields.Integer('Cupos OPSU', default=0)
    cupos_especiales = fields.Integer('Cupos Especiales', default=0)
    
    # Contadores para seguimiento
    count_preinscritos = fields.Integer('Total Preinscritos', compute='_compute_count_preinscritos')
    count_inscritos = fields.Integer('Total Inscritos', compute='_compute_count_inscritos')
    
    # Relaciones para accesos rápidos
    preinscripcion_ids = fields.One2many('admision.preinscripcion', 'proceso_id', string='Preinscripciones')
    inscripcion_ids = fields.One2many('admision.inscripcion', 'proceso_id', string='Inscripciones')
    
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin and record.fecha_inicio > record.fecha_fin:
                raise ValidationError(_("La fecha de inicio no puede ser posterior a la fecha de cierre."))

    def _compute_count_preinscritos(self):
        for record in self:
            record.count_preinscritos = len(record.preinscripcion_ids)
    
    def _compute_count_inscritos(self):
        for record in self:
            record.count_inscritos = len(record.inscripcion_ids)

    @api.constrains('state', 'tipo', 'periodo_id')
    def _check_unique_active_process(self):
        for record in self:
            if record.state == 'active':
                same_type = self.search([
                    ('id', '!=', record.id),
                    ('tipo', '=', record.tipo),
                    ('periodo_id', '=', record.periodo_id.id),
                    ('state', '=', 'active')
                ])
                if same_type:
                    raise ValidationError(_("Ya existe un proceso activo del mismo tipo para este periodo."))

    def action_activar(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'active'
    
    def action_cerrar(self):
        for record in self:
            if record.state == 'active':
                record.state = 'closed'
    
    def action_ver_preinscritos(self):
        self.ensure_one()
        return {
            'name': _('Aspirantes Preinscritos'),
            'view_mode': 'list,form',
            'res_model': 'admision.preinscripcion',
            'domain': [('proceso_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_proceso_id': self.id}
        }
    
    def action_ver_inscritos(self):
        self.ensure_one()
        return {
            'name': _('Estudiantes Inscritos'),
            'view_mode': 'list,form',
            'res_model': 'admision.inscripcion',
            'domain': [('proceso_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_proceso_id': self.id}
        }


class AdmisionPeriodo(models.Model):
    _name = 'admision.periodo'
    _description = 'Periodo Académico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_inicio desc, name'
    
    name = fields.Char('Nombre', required=True, help="Ej: 2026-1", tracking=True)
    fecha_inicio = fields.Date('Fecha de Inicio', required=True, tracking=True)
    fecha_fin = fields.Date('Fecha de Finalización', required=True, tracking=True)
    active = fields.Boolean('Activo', default=True, tracking=True)
    description = fields.Text('Descripción', tracking=True)
    
    proceso_ids = fields.One2many('admision.proceso', 'periodo_id', string='Procesos')
    
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for record in self:
            if record.fecha_inicio and record.fecha_fin and record.fecha_inicio > record.fecha_fin:
                raise ValidationError(_("La fecha de inicio no puede ser posterior a la fecha de finalización."))
    
    @api.constrains('active')
    def _check_unique_active(self):
        if self.filtered(lambda p: p.active):
            active_periods = self.search([('active', '=', True), ('id', 'not in', self.ids)])
            if active_periods:
                raise ValidationError(_("Solo puede haber un periodo académico activo a la vez."))