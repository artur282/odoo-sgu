# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AdmisionPrograma(models.Model):
    _name = 'admision.programa'
    _description = 'Programa Académico'
    _order = 'name'
    
    name = fields.Char('Nombre del Programa', required=True)
    code = fields.Char('Código', required=True)
    facultad = fields.Char('Facultad/Decanato', required=True)
    nivel = fields.Selection([
        ('pregrado', 'Pregrado'),
        ('postgrado', 'Postgrado'),
        ('extension', 'Extensión')
    ], string='Nivel', required=True, default='pregrado')
    duracion = fields.Integer('Duración (Semestres)', default=10)
    description = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)
    
    # Relaciones
    sede_ids = fields.Many2many('admision.sede', string='Sedes Disponibles')
    seccion_ids = fields.One2many('admision.seccion', 'programa_id', string='Secciones')
    aspirante_ids = fields.One2many('admision.aspirante', 'programa_id', string='Aspirantes')
    
    # Contadores para estadísticas
    count_aspirantes = fields.Integer('Total Aspirantes', compute='_compute_count_aspirantes')
    count_preinscritos = fields.Integer('Total Preinscritos', compute='_compute_count_preinscritos')
    count_inscritos = fields.Integer('Total Inscritos', compute='_compute_count_inscritos')
    count_estudiantes = fields.Integer('Total Estudiantes', compute='_compute_count_estudiantes')
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código del programa debe ser único.')
    ]
    
    def _compute_count_aspirantes(self):
        for record in self:
            record.count_aspirantes = self.env['admision.aspirante'].search_count([
                ('programa_id', '=', record.id)
            ])
    
    def _compute_count_preinscritos(self):
        for record in self:
            record.count_preinscritos = self.env['admision.aspirante'].search_count([
                ('programa_id', '=', record.id),
                ('state', '=', 'preinscrito')
            ])
    
    def _compute_count_inscritos(self):
        for record in self:
            record.count_inscritos = self.env['admision.aspirante'].search_count([
                ('programa_id', '=', record.id),
                ('state', '=', 'inscrito')
            ])
    
    def _compute_count_estudiantes(self):
        for record in self:
            record.count_estudiantes = self.env['admision.aspirante'].search_count([
                ('programa_id', '=', record.id),
                ('state', '=', 'estudiante')
            ])
    
    def action_ver_aspirantes(self):
        self.ensure_one()
        return {
            'name': _('Aspirantes'),
            'view_mode': 'list,form',
            'res_model': 'admision.aspirante',
            'domain': [('programa_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_programa_id': self.id}
        }
    
    def action_ver_preinscritos(self):
        self.ensure_one()
        return {
            'name': _('Aspirantes Preinscritos'),
            'view_mode': 'list,form',
            'res_model': 'admision.aspirante',
            'domain': [('programa_id', '=', self.id), ('state', '=', 'preinscrito')],
            'type': 'ir.actions.act_window',
            'context': {'default_programa_id': self.id}
        }
    
    def action_ver_inscritos(self):
        self.ensure_one()
        return {
            'name': _('Aspirantes Inscritos'),
            'view_mode': 'list,form',
            'res_model': 'admision.aspirante',
            'domain': [('programa_id', '=', self.id), ('state', '=', 'inscrito')],
            'type': 'ir.actions.act_window',
            'context': {'default_programa_id': self.id}
        }
    
    def action_ver_estudiantes(self):
        self.ensure_one()
        return {
            'name': _('Estudiantes'),
            'view_mode': 'list,form',
            'res_model': 'admision.aspirante',
            'domain': [('programa_id', '=', self.id), ('state', '=', 'estudiante')],
            'type': 'ir.actions.act_window',
            'context': {'default_programa_id': self.id}
        }