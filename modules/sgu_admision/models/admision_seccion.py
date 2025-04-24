# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AdmisionSeccion(models.Model):
    _name = 'admision.seccion'
    _description = 'Sección'
    _order = 'name'
    
    name = fields.Char('Nombre/Código Sección', required=True)
    programa_id = fields.Many2one('admision.programa', string='Programa', required=True)
    sede_id = fields.Many2one('admision.sede', string='Sede', required=True,
                             domain="[('id', 'in', sede_disponible_ids)]")
    sede_disponible_ids = fields.Many2many('admision.sede', compute='_compute_sede_disponible')
    
    periodo_id = fields.Many2one('admision.periodo', string='Periodo Académico', required=True)
    capacidad = fields.Integer('Capacidad Máxima', required=True, default=40)
    capacidad_restante = fields.Integer('Cupos Disponibles', compute='_compute_capacidad_restante', store=True)
    
    # Relaciones
    inscripcion_ids = fields.One2many('admision.inscripcion', 'seccion_id', string='Inscripciones')
    horario_ids = fields.One2many('admision.horario', 'seccion_id', string='Horarios')
    
    active = fields.Boolean('Activo', default=True)
    
    _sql_constraints = [
        ('name_programa_periodo_uniq', 'unique(name, programa_id, periodo_id)', 
         'Ya existe una sección con este nombre para este programa y periodo.')
    ]
    
    @api.depends('programa_id')
    def _compute_sede_disponible(self):
        for record in self:
            if record.programa_id:
                record.sede_disponible_ids = record.programa_id.sede_ids
            else:
                record.sede_disponible_ids = False
    
    @api.depends('capacidad', 'inscripcion_ids')
    def _compute_capacidad_restante(self):
        for record in self:
            inscritos = len(record.inscripcion_ids.filtered(lambda i: i.state == 'confirmed'))
            record.capacidad_restante = max(0, record.capacidad - inscritos)
    
    @api.constrains('capacidad')
    def _check_capacidad(self):
        for record in self:
            if record.capacidad <= 0:
                raise ValidationError(_("La capacidad debe ser mayor a cero."))
    
    def action_ver_inscritos(self):
        self.ensure_one()
        return {
            'name': _('Estudiantes Inscritos'),
            'view_mode': 'list,form',
            'res_model': 'admision.inscripcion',
            'domain': [('seccion_id', '=', self.id), ('state', '=', 'confirmed')],
            'type': 'ir.actions.act_window',
            'context': {'default_seccion_id': self.id}
        }
    
    def action_ver_horarios(self):
        self.ensure_one()
        return {
            'name': _('Horarios'),
            'view_mode': 'list,form',
            'res_model': 'admision.horario',
            'domain': [('seccion_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_seccion_id': self.id}
        }