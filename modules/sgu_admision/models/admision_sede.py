# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AdmisionSede(models.Model):
    _name = 'admision.sede'
    _description = 'Sede'
    _order = 'name'
    
    name = fields.Char('Nombre de la Sede', required=True)
    code = fields.Char('Código', required=True)
    direccion = fields.Text('Dirección', required=True)
    municipio = fields.Char('Municipio', required=True)
    estado = fields.Char('Estado', required=True)
    telefono = fields.Char('Teléfono')
    email = fields.Char('Correo Electrónico')
    director = fields.Char('Director')
    active = fields.Boolean('Activo', default=True)
    
    # Relaciones
    programa_ids = fields.Many2many('admision.programa', string='Programas Disponibles')
    aspirante_ids = fields.One2many('admision.aspirante', 'sede_id', string='Aspirantes')
    
    # Contadores para estadísticas
    count_aspirantes = fields.Integer('Total Aspirantes', compute='_compute_count_aspirantes')
    count_preinscritos = fields.Integer('Total Preinscritos', compute='_compute_count_preinscritos')
    count_inscritos = fields.Integer('Total Inscritos', compute='_compute_count_inscritos')
    count_estudiantes = fields.Integer('Total Estudiantes', compute='_compute_count_estudiantes')
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código de la sede debe ser único.')
    ]
    
    def _compute_count_aspirantes(self):
        for record in self:
            record.count_aspirantes = self.env['admision.aspirante'].search_count([
                ('sede_id', '=', record.id)
            ])
    
    def _compute_count_preinscritos(self):
        for record in self:
            record.count_preinscritos = self.env['admision.aspirante'].search_count([
                ('sede_id', '=', record.id),
                ('state', '=', 'preinscrito')
            ])
    
    def _compute_count_inscritos(self):
        for record in self:
            record.count_inscritos = self.env['admision.aspirante'].search_count([
                ('sede_id', '=', record.id),
                ('state', '=', 'inscrito')
            ])
    
    def _compute_count_estudiantes(self):
        for record in self:
            record.count_estudiantes = self.env['admision.aspirante'].search_count([
                ('sede_id', '=', record.id),
                ('state', '=', 'estudiante')
            ])
    
    def action_ver_aspirantes(self):
        self.ensure_one()
        return {
            'name': _('Aspirantes'),
            'view_mode': 'list,form',
            'res_model': 'admision.aspirante',
            'domain': [('sede_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_sede_id': self.id}
        }