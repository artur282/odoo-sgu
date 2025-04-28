# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class AdmisionAspirante(models.Model):
    _name = 'admision.aspirante'
    _description = 'Aspirante'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'
    
    partner_id = fields.Many2one('res.partner', string='Contacto', required=True, 
                                 tracking=True, ondelete='cascade')
    
    # Campos relacionados del partner para la vista
    email = fields.Char(related='partner_id.email', string='Correo Electrónico', readonly=False)
    phone = fields.Char(related='partner_id.phone', string='Teléfono', readonly=False)
    mobile = fields.Char(related='partner_id.mobile', string='Móvil', readonly=False)
    street = fields.Char(related='partner_id.street', string='Calle', readonly=False)
    street2 = fields.Char(related='partner_id.street2', string='Calle 2', readonly=False)
    city = fields.Char(related='partner_id.city', string='Ciudad', readonly=False)
    state_id = fields.Many2one(related='partner_id.state_id', string='Estado/Provincia', readonly=False)
    zip = fields.Char(related='partner_id.zip', string='Código Postal', readonly=False)
    country_id = fields.Many2one(related='partner_id.country_id', string='País', readonly=False)

    # Información personal básica (gestionada a través del partner)
    cedula = fields.Char('Cédula de Identidad', required=True, tracking=True, 
                         help="Formato: V-12345678 o E-12345678")
    display_name = fields.Char(compute='_compute_display_name', store=True, readonly=False)
    
    # Datos complementarios
    fecha_nacimiento = fields.Date('Fecha de Nacimiento', tracking=True)
    sexo = fields.Selection([
        ('m', 'Masculino'),
        ('f', 'Femenino')
    ], string='Sexo', tracking=True)
    etnia = fields.Char('Etnia', tracking=True)
    discapacidad = fields.Boolean('Posee Discapacidad', tracking=True, default=False)
    tipo_discapacidad = fields.Char('Tipo de Discapacidad', tracking=True)
    
    # Tipo de asignación
    tipo_asignacion = fields.Selection([
        ('opsu', 'OPSU'),
        ('rector', 'Rector'),
        ('secretaria', 'Secretaria'),
        ('dace', 'DACE'),
        ('aspirante', 'Aspirante a Cupo')
    ], string='Tipo de Asignación', required=True, tracking=True, default='aspirante')
    codigo_opsu = fields.Char('Código OPSU', tracking=True, 
                              help="Código de identificación asignado por la OPSU")
    
    # Asignación de programa y sede
    programa_id = fields.Many2one('admision.programa', string='Programa/Carrera', required=True, tracking=True)
    sede_id = fields.Many2one('admision.sede', string='Sede', required=True, tracking=True)
    
    # Estado del aspirante en el sistema
    state = fields.Selection([
        ('registrado', 'Registrado'),
        ('preinscrito', 'Preinscrito'),
        ('inscrito', 'Inscrito'),
        ('estudiante', 'Estudiante Activo')
    ], string='Estado', default='registrado', tracking=True)
    
    # Campos de documentación
    documentos_completos = fields.Boolean('Documentos Completos', tracking=True, default=False)
    notas_documentos = fields.Text('Notas sobre Documentos', tracking=True)
    
    # Relaciones con otros modelos
    preinscripcion_ids = fields.One2many('admision.preinscripcion', 'aspirante_id', string='Preinscripciones')
    inscripcion_ids = fields.One2many('admision.inscripcion', 'aspirante_id', string='Inscripciones')
    
    _sql_constraints = [
        ('cedula_uniq', 'unique(cedula)', 'Ya existe un aspirante con esta cédula de identidad.')
    ]
    
    @api.depends('partner_id.name', 'cedula')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id and record.cedula:
                record.display_name = f"{record.partner_id.name} ({record.cedula})"
            elif record.partner_id:
                record.display_name = record.partner_id.name
            else:
                record.display_name = record.cedula or ""
    
    @api.constrains('cedula')
    def _check_cedula_format(self):
        for record in self:
            if record.cedula:
                # Formato: V-12345678 o E-12345678
                if not re.match(r'^[VE]-\d{5,10}$', record.cedula):
                    raise ValidationError(_("El formato de la cédula debe ser V-XXXXXXXX o E-XXXXXXXX"))
    
    @api.model_create_multi
    def create(self, vals_list):
        result = []
        for vals in vals_list:
            # Si viene del portal como aspirante, se crea como tipo 'aspirante'
            if self.env.context.get('portal'):
                vals['tipo_asignacion'] = 'aspirante'
            
            # Crear o vincular con un partner
            if not vals.get('partner_id'):
                partner_vals = {
                    'name': vals.get('name', 'Nuevo Aspirante'),
                    'email': vals.get('email'),
                    'phone': vals.get('phone'),
                    'mobile': vals.get('mobile'),
                }
                partner = self.env['res.partner'].create(partner_vals)
                vals['partner_id'] = partner.id
        
        return super(AdmisionAspirante, self).create(vals_list)
    
    def action_convertir_estudiante(self):
        """Convierte al aspirante en estudiante"""
        for record in self:
            if record.state == 'inscrito':
                # Asignar grupo de estudiante al usuario vinculado
                if record.partner_id.user_id:
                    user = record.partner_id.user_id
                    estudiante_group = self.env.ref('admision.group_estudiante')
                    aspirante_group = self.env.ref('admision.group_aspirante')
                    
                    # Quitar grupo aspirante y agregar grupo estudiante
                    if aspirante_group in user.groups_id:
                        user.write({'groups_id': [(3, aspirante_group.id)]})
                    user.write({'groups_id': [(4, estudiante_group.id)]})
                
                record.state = 'estudiante'
    
    def action_ver_preinscripciones(self):
        self.ensure_one()
        return {
            'name': _('Preinscripciones'),
            'view_mode': 'list,form',
            'res_model': 'admision.preinscripcion',
            'domain': [('aspirante_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_aspirante_id': self.id}
        }
    
    def action_ver_inscripciones(self):
        self.ensure_one()
        return {
            'name': _('Inscripciones'),
            'view_mode': 'list,form',
            'res_model': 'admision.inscripcion',
            'domain': [('aspirante_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'context': {'default_aspirante_id': self.id}
        }