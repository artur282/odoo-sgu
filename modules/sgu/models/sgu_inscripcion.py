# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Inscripcion(models.Model):
    _name = 'sgu.inscripcion'
    _description = 'Inscripción formal'
    _rec_name = 'numero_inscripcion'

    numero_inscripcion = fields.Char('Número', readonly=True, copy=False)
    aspirante_id = fields.Many2one('sgu.aspirante', 'Aspirante', required=True, tracking=True)
    proceso_id = fields.Many2one('sgu.proceso', 'Proceso', required=True,
                               domain="[('tipo', '=', 'inscripcion'), ('state', '=', 'active')]")
    fecha_inscripcion = fields.Date('Fecha', default=fields.Date.today)

    # Referencias a modelos base
    carrera_id = fields.Many2one(related='aspirante_id.carrera_id', readonly=True)
    sede_id = fields.Many2one(related='aspirante_id.sede_id', readonly=True)

    # Sección asignada
    seccion_id = fields.Many2one('sgu.seccion', 'Sección', required=True, 
                                domain="[('carrera_id', '=', carrera_id), ('sede_id', '=', sede_id)]")

    # Estado de la inscripción
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada')
    ], string='Estado', default='draft', tracking=True)

    # Documentación
    doc_cedula = fields.Boolean('Cédula entregada')
    doc_titulo = fields.Boolean('Título entregado')
    doc_notas = fields.Boolean('Notas entregadas')
    doc_fotos = fields.Boolean('Fotos entregadas')
    doc_partida = fields.Boolean('Partida de nacimiento')
    documentacion_completa = fields.Boolean('Documentos completos', compute='_compute_documentacion', store=True)


    # Usuario que registró la inscripción
    usuario_inscripcion_id = fields.Many2one('res.users', 'Registrado por', default=lambda self: self.env.user)
    
    # Campos adicionales según requerimientos
    numero_expediente = fields.Char('Número de expediente', readonly=True)
    registro_opsu_entregado = fields.Boolean('Registro OPSU entregado')
    
    @api.depends('doc_cedula', 'doc_titulo', 'doc_notas', 'doc_fotos', 'doc_partida', 'registro_opsu_entregado')
    def _compute_documentacion(self):
        for record in self:
            record.documentacion_completa = all([
                record.doc_cedula, record.doc_titulo, record.doc_notas,
                record.doc_fotos, record.doc_partida, record.registro_opsu_entregado
            ])
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numero_inscripcion'):
                vals['numero_inscripcion'] = self.env['ir.sequence'].next_by_code('sgu.inscripcion.sequence') or 'INS/00000'
        result = super(Inscripcion, self).create(vals_list)
        # Generar número de expediente para cada inscripción creada
        for record in result:
            record.generar_numero_expediente()
        return result
    
    def generar_numero_expediente(self):
        """Generar un número de expediente único"""
        self.ensure_one()
        if not self.numero_expediente and self.proceso_id and self.carrera_id and self.sede_id:
            # Formato: YYYY-P(periodo)-SEDE-PROGRAMA-NNN
            # Ejemplo: 2026-1-SJM-MED-001
            periodo = self.proceso_id.periodo_id
            codigo_periodo = f"{periodo.anio}-{periodo.periodo}"
            codigo_sede = self.sede_id.codigo_sede or 'SEDE'
            codigo_programa = self.carrera_id.codigo or 'PROG'
            
            # Buscar el último número
            ultimo_expediente = self.search([
                ('carrera_id', '=', self.carrera_id.id),
                ('sede_id', '=', self.sede_id.id),
                ('proceso_id.periodo_id', '=', periodo.id)
            ], order='id desc', limit=1).numero_expediente
            
            # Extraer el número del último expediente o iniciar en 1
            if ultimo_expediente and '-' in ultimo_expediente:
                ultimo_numero = int(ultimo_expediente.split('-')[-1])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
            
            self.numero_expediente = f"{codigo_periodo}-{codigo_sede}-{codigo_programa}-{nuevo_numero:03d}"
            
    def action_confirm(self):
        """Confirmar la inscripción"""
        for record in self:
            if not record.documentacion_completa:
                return {
                    'warning': {
                        'title': 'Documentación incompleta',
                        'message': 'No se puede confirmar la inscripción porque la documentación está incompleta.'
                    }
                }
            
            if record.seccion_id.capacidad_restante <= 0:
                return {
                    'warning': {
                        'title': 'Sección llena',
                        'message': 'No hay cupos disponibles en la sección seleccionada.'
                    }
                }
                
            record.state = 'confirmed'
            # Actualizar el estado del aspirante
            record.aspirante_id.state = 'inscrito'
            
    def print_constancia(self):
        """Imprimir constancia de inscripción"""
        self.ensure_one()
        return self.env.ref('sgu.action_report_sgu_constancia_inscripcion').report_action(self)
        
    def convertir_a_estudiante(self):
        """Convertir al aspirante en estudiante"""
        self.ensure_one()
        return self.aspirante_id.crear_estudiante()
