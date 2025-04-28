# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime

class AdmisionInscripcion(models.Model):
    _name = 'admision.inscripcion'
    _description = 'Inscripción'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'numero_inscripcion'
    _order = 'create_date desc'
    
    numero_inscripcion = fields.Char('Número de Inscripción', readonly=True, copy=False)
    aspirante_id = fields.Many2one('admision.aspirante', string='Aspirante', required=True, 
                                  tracking=True, ondelete='restrict')
    proceso_id = fields.Many2one('admision.proceso', string='Proceso de Inscripción', 
                                domain="[('tipo', '=', 'inscripcion'), ('state', '=', 'active')]",
                                required=True, tracking=True)
    
    fecha_inscripcion = fields.Date('Fecha de Inscripción', default=fields.Date.today, tracking=True)
    
    # Datos académicos
    programa_id = fields.Many2one('admision.programa', string='Programa/Carrera', 
                                 related='aspirante_id.programa_id', readonly=True)
    sede_id = fields.Many2one('admision.sede', string='Sede', 
                             related='aspirante_id.sede_id', readonly=True)
    seccion_id = fields.Many2one('admision.seccion', string='Sección', 
                              domain="[('programa_id', '=', programa_id)]", required=True, tracking=True)
    
    # Estado de la inscripción
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada')
    ], string='Estado', default='draft', tracking=True)
    
    # Usuario que realizó la inscripción (operador)
    usuario_inscripcion_id = fields.Many2one('res.users', string='Realizado por', 
                                           default=lambda self: self.env.user, readonly=True)
    
    # Documentación entregada
    doc_cedula = fields.Boolean('Cédula de Identidad', tracking=True)
    doc_titulo = fields.Boolean('Título de Bachiller', tracking=True)
    doc_notas = fields.Boolean('Notas Certificadas', tracking=True)
    doc_fotos = fields.Boolean('Fotos', tracking=True)
    doc_partida = fields.Boolean('Partida de Nacimiento', tracking=True)
    doc_otros = fields.Boolean('Otros Documentos', tracking=True)
    
    documentacion_completa = fields.Boolean('Documentación Completa', compute='_compute_documentacion_completa', 
                                          store=True)
    
    nota_documental = fields.Text('Observaciones Documentales', tracking=True)
    
    # Datos de la preinscripción
    preinscripcion_id = fields.Many2one('admision.preinscripcion', string='Preinscripción', 
                                      domain="[('aspirante_id', '=', aspirante_id), ('state', '=', 'confirmed')]")
    
    _sql_constraints = [
        ('aspirante_proceso_uniq', 'unique(aspirante_id, proceso_id)', 
         'El aspirante ya tiene una inscripción para este proceso.')
    ]
    
    @api.depends('doc_cedula', 'doc_titulo', 'doc_notas', 'doc_fotos', 'doc_partida')
    def _compute_documentacion_completa(self):
        for record in self:
            record.documentacion_completa = (
                record.doc_cedula and 
                record.doc_titulo and 
                record.doc_notas and 
                record.doc_fotos and 
                record.doc_partida
            )
    
    @api.onchange('aspirante_id')
    def _onchange_aspirante_id(self):
        if self.aspirante_id:
            # Buscar la preinscripción confirmada más reciente
            preinscripcion = self.env['admision.preinscripcion'].search([
                ('aspirante_id', '=', self.aspirante_id.id),
                ('state', '=', 'confirmed')
            ], limit=1, order='create_date DESC')
            
            if preinscripcion:
                self.preinscripcion_id = preinscripcion.id
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Asignar número de inscripción
            if not vals.get('numero_inscripcion'):
                vals['numero_inscripcion'] = self.env['ir.sequence'].next_by_code('admision.inscripcion')
            
            # Verificar que el proceso esté activo
            proceso = self.env['admision.proceso'].browse(vals.get('proceso_id'))
            if proceso.state != 'active':
                raise UserError(_('No se puede realizar inscripción en un proceso inactivo.'))
            
            # Verificar que la fecha esté dentro del rango del proceso
            hoy = date.today()
            if hoy < proceso.fecha_inicio or hoy > proceso.fecha_fin:
                raise UserError(_('El proceso de inscripción no está disponible en esta fecha.'))
        
        return super(AdmisionInscripcion, self).create(vals_list)
    
    def action_confirmar(self):
        for record in self:
            if record.state == 'draft':
                # Verificar documentación completa
                if not record.documentacion_completa:
                    raise UserError(_('No se puede confirmar la inscripción sin la documentación completa.'))
                
                # Actualizar estado del aspirante
                record.aspirante_id.write({
                    'state': 'inscrito',
                    'documentos_completos': True
                })
                
                # Confirmar inscripción
                record.state = 'confirmed'
    
    def action_convertir_estudiante(self):
        for record in self:
            if record.state == 'confirmed':
                record.aspirante_id.action_convertir_estudiante()
    
    def action_imprimir_constancia(self):
        self.ensure_one()
        # Corregir el nombre del módulo en la referencia del XML ID
        return self.env.ref('sgu_admision.action_report_inscripcion').report_action(self)