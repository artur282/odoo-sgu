# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date

class AdmisionPreinscripcion(models.Model):
    _name = 'admision.preinscripcion'
    _description = 'Preinscripción'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'numero_preinscripcion'
    _order = 'create_date desc'
    
    numero_preinscripcion = fields.Char('Número de Preinscripción', readonly=True, copy=False)
    aspirante_id = fields.Many2one('admision.aspirante', string='Aspirante', required=True, 
                                  tracking=True, ondelete='cascade')
    proceso_id = fields.Many2one('admision.proceso', string='Proceso de Preinscripción', 
                                domain="[('tipo', '=', 'preinscripcion'), ('state', '=', 'active')]",
                                required=True, tracking=True)
    
    fecha_preinscripcion = fields.Date('Fecha de Preinscripción', default=fields.Date.today, tracking=True)
    
    # Datos académicos
    programa_id = fields.Many2one('admision.programa', string='Programa/Carrera', 
                                 related='aspirante_id.programa_id', readonly=True)
    sede_id = fields.Many2one('admision.sede', string='Sede', 
                             related='aspirante_id.sede_id', readonly=True)
    
    # Estado de la preinscripción
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada')
    ], string='Estado', default='draft', tracking=True)
    
    # Campos académicos adicionales
    promedio_bachillerato = fields.Float('Promedio de Bachillerato', tracking=True)
    ano_graduacion = fields.Integer('Año de Graduación', tracking=True)
    institucion_procedencia = fields.Char('Institución de Procedencia', tracking=True)
    
    # Datos socioeconómicos
    ingreso_familiar = fields.Selection([
        ('bajo', 'Bajo'),
        ('medio_bajo', 'Medio Bajo'),
        ('medio', 'Medio'),
        ('medio_alto', 'Medio Alto'),
        ('alto', 'Alto')
    ], string='Ingreso Familiar', tracking=True)
    trabaja = fields.Boolean('Trabaja Actualmente', tracking=True)
    empresa_trabajo = fields.Char('Empresa donde Trabaja', tracking=True)
    
    # Dirección completa
    direccion_completa = fields.Text('Dirección Completa', tracking=True)
    estado = fields.Char('Estado', tracking=True)
    municipio = fields.Char('Municipio', tracking=True)
    parroquia = fields.Char('Parroquia', tracking=True)
    codigo_postal = fields.Char('Código Postal', tracking=True)
    
    # Contacto de emergencia
    contacto_emergencia = fields.Char('Nombre Contacto de Emergencia', tracking=True)
    telefono_emergencia = fields.Char('Teléfono de Emergencia', tracking=True)
    relacion_contacto = fields.Char('Relación con el Contacto', tracking=True)
    
    _sql_constraints = [
        ('aspirante_proceso_uniq', 'unique(aspirante_id, proceso_id)', 
         'El aspirante ya tiene una preinscripción para este proceso.')
    ]
    
    @api.model_create_multi
    def create(self, vals_list):
        results = []
        for vals in vals_list:
            # Asignar número de preinscripción
            if not vals.get('numero_preinscripcion'):
                vals['numero_preinscripcion'] = self.env['ir.sequence'].next_by_code('admision.preinscripcion')
            
            # Verificar que el proceso esté activo
            proceso = self.env['admision.proceso'].browse(vals.get('proceso_id'))
            if proceso.state != 'active':
                raise UserError(_('No se puede realizar preinscripción en un proceso inactivo.'))
            
            # Verificar que la fecha esté dentro del rango del proceso
            hoy = date.today()
            if hoy < proceso.fecha_inicio or hoy > proceso.fecha_fin:
                raise UserError(_('El proceso de preinscripción no está disponible en esta fecha.'))
        
        return super(AdmisionPreinscripcion, self).create(vals_list)
    
    def action_confirmar(self):
        for record in self:
            if record.state == 'draft':
                # Actualizar estado del aspirante
                record.aspirante_id.write({'state': 'preinscrito'})
                record.state = 'confirmed'
    
    def action_imprimir_comprobante(self):
        self.ensure_one()
        return self.env.ref('admision.action_report_preinscripcion').report_action(self)
    
    def action_borrador(self):
        for record in self:
            if record.state == 'confirmed':
                record.state = 'draft'