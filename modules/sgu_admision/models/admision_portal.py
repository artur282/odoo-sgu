# -*- coding: utf-8 -*-

from odoo import models, fields, api, http, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request
import logging
import uuid
from datetime import date

_logger = logging.getLogger(__name__)

class AdmisionPortalMixin(models.AbstractModel):
    _name = 'admision.portal.mixin'
    _description = 'Portal Mixin para Admisión'

    def _admision_portal_ensure_token(self):
        """ Este método genera un token único para acceso por portal si no existe """
        if not self.access_token:
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token


class AdmisionPortal(http.Controller):
    def _prepare_portal_layout_values(self):
        values = {}
        
        # Si el usuario está autenticado, verificar si es aspirante o estudiante
        if not request.env.user._is_public():
            partner = request.env.user.partner_id
            
            aspirante = request.env['admision.aspirante'].sudo().search([
                ('partner_id', '=', partner.id)
            ], limit=1)
            
            values['is_aspirante'] = bool(aspirante)
            values['aspirante'] = aspirante if aspirante else False
            values['is_estudiante'] = aspirante and aspirante.state == 'estudiante'
        
        return values
    
    @http.route(['/mi/admision', '/my/admission'], type='http', auth="user", website=True)
    def portal_mi_admision(self, **kw):
        values = self._prepare_portal_layout_values()
        
        if values.get('is_aspirante'):
            aspirante = values['aspirante']
            
            # Recuperar preinscripción más reciente (si existe)
            preinscripcion = request.env['admision.preinscripcion'].sudo().search([
                ('aspirante_id', '=', aspirante.id)
            ], limit=1, order='create_date DESC')
            
            # Recuperar inscripción más reciente (si existe)
            inscripcion = request.env['admision.inscripcion'].sudo().search([
                ('aspirante_id', '=', aspirante.id)
            ], limit=1, order='create_date DESC')
            
            # Si es estudiante, recuperar horarios
            horarios = False
            if values.get('is_estudiante') and inscripcion:
                horarios = request.env['admision.horario'].sudo().search([
                    ('seccion_id', '=', inscripcion.seccion_id.id)
                ], order='dia_semana, hora_inicio')
            
            values.update({
                'preinscripcion': preinscripcion if preinscripcion else False,
                'inscripcion': inscripcion if inscripcion else False,
                'horarios': horarios if horarios else False,
                'page_name': 'admision',
            })
        
        return request.render("admision.portal_mi_admision", values)
    
    @http.route(['/mi/admision/preinscripcion/nueva'], type='http', auth="user", website=True)
    def portal_nueva_preinscripcion(self, **kw):
        values = self._prepare_portal_layout_values()
        
        if not values.get('is_aspirante'):
            return request.redirect('/mi/admision')
        
        aspirante = values['aspirante']
        
        # Verificar si el aspirante ya tiene una preinscripción en un proceso activo
        preinscripcion = request.env['admision.preinscripcion'].sudo().search([
            ('aspirante_id', '=', aspirante.id),
            ('proceso_id.state', '=', 'active')
        ], limit=1)
        
        if preinscripcion:
            # Redirigir a editar la preinscripción existente
            return request.redirect(f'/mi/admision/preinscripcion/{preinscripcion.id}')
        
        # Buscar procesos de preinscripción activos
        procesos = request.env['admision.proceso'].sudo().search([
            ('tipo', '=', 'preinscripcion'),
            ('state', '=', 'active'),
            '|',
                ('programa_ids', '=', False),
                ('programa_ids', 'in', aspirante.programa_id.id)
        ])
        
        if not procesos:
            values['no_active_process'] = True
            return request.render("admision.portal_no_proceso_activo", values)
        
        # Seleccionar el primer proceso activo o el específico para el programa
        proceso = procesos.filtered(lambda p: aspirante.programa_id in p.programa_ids)
        if not proceso:
            proceso = procesos[0]
        
        values.update({
            'proceso': proceso,
            'page_name': 'nueva_preinscripcion',
        })
        
        return request.render("admision.portal_nueva_preinscripcion", values)

    @http.route(['/mi/admision/preinscripcion/<int:preinscripcion_id>'], type='http', auth="user", website=True)
    def portal_ver_preinscripcion(self, preinscripcion_id, **kw):
        values = self._prepare_portal_layout_values()
        
        if not values.get('is_aspirante'):
            return request.redirect('/mi/admision')
        
        aspirante = values['aspirante']
        
        # Recuperar la preinscripción específica
        preinscripcion = request.env['admision.preinscripcion'].sudo().search([
            ('id', '=', preinscripcion_id),
            ('aspirante_id', '=', aspirante.id)
        ], limit=1)
        
        if not preinscripcion:
            return request.redirect('/mi/admision')
        
        values.update({
            'preinscripcion': preinscripcion,
            'page_name': 'ver_preinscripcion',
        })
        
        return request.render("admision.portal_ver_preinscripcion", values)
    
    @http.route(['/mi/admision/preinscripcion/enviar'], type='http', auth="user", website=True, methods=['POST'])
    def portal_submit_preinscripcion(self, **kw):
        values = self._prepare_portal_layout_values()
        
        if not values.get('is_aspirante'):
            return request.redirect('/mi/admision')
        
        aspirante = values['aspirante']
        proceso_id = int(kw.get('proceso_id', 0))
        
        # Verificar que el proceso exista y esté activo
        proceso = request.env['admision.proceso'].sudo().browse(proceso_id)
        if not proceso or proceso.state != 'active' or proceso.tipo != 'preinscripcion':
            return request.redirect('/mi/admision')
        
        # Crear o actualizar la preinscripción
        preinscripcion_vals = {
            'aspirante_id': aspirante.id,
            'proceso_id': proceso.id,
            'fecha_preinscripcion': date.today(),
            'promedio_bachillerato': float(kw.get('promedio_bachillerato', 0)),
            'ano_graduacion': int(kw.get('ano_graduacion', 0)),
            'institucion_procedencia': kw.get('institucion_procedencia'),
            'ingreso_familiar': kw.get('ingreso_familiar'),
            'trabaja': kw.get('trabaja') == 'on',
            'empresa_trabajo': kw.get('empresa_trabajo'),
            'direccion_completa': kw.get('direccion_completa'),
            'estado': kw.get('estado'),
            'municipio': kw.get('municipio'),
            'parroquia': kw.get('parroquia'),
            'codigo_postal': kw.get('codigo_postal'),
            'contacto_emergencia': kw.get('contacto_emergencia'),
            'telefono_emergencia': kw.get('telefono_emergencia'),
            'relacion_contacto': kw.get('relacion_contacto'),
        }
        
        # Verificar si ya existe una preinscripción para este proceso
        preinscripcion = request.env['admision.preinscripcion'].sudo().search([
            ('aspirante_id', '=', aspirante.id),
            ('proceso_id', '=', proceso.id)
        ], limit=1)
        
        try:
            if preinscripcion:
                # Actualizar preinscripción existente
                preinscripcion.sudo().write(preinscripcion_vals)
            else:
                # Crear nueva preinscripción
                preinscripcion = request.env['admision.preinscripcion'].sudo().create(preinscripcion_vals)
                
            # Confirmar la preinscripción
            preinscripcion.sudo().action_confirmar()
            
            return request.redirect(f'/mi/admision/preinscripcion/{preinscripcion.id}?success=1')
            
        except Exception as e:
            values.update({
                'error_message': str(e),
                'proceso': proceso,
                'page_name': 'nueva_preinscripcion',
                'form_data': kw,
            })
            return request.render("admision.portal_nueva_preinscripcion", values)
    
    @http.route(['/mi/admision/constancia/<string:tipo>/<int:registro_id>'], type='http', auth="user", website=True)
    def portal_imprimir_constancia(self, tipo, registro_id, **kw):
        values = self._prepare_portal_layout_values()
        
        if not values.get('is_aspirante') and not values.get('is_estudiante'):
            return request.redirect('/mi/admision')
        
        aspirante = values['aspirante']
        
        if tipo == 'preinscripcion':
            # Recuperar la preinscripción específica
            preinscripcion = request.env['admision.preinscripcion'].sudo().search([
                ('id', '=', registro_id),
                ('aspirante_id', '=', aspirante.id)
            ], limit=1)
            
            if not preinscripcion:
                return request.redirect('/mi/admision')
            
            return request.env.ref('admision.action_report_preinscripcion').with_context(
                download=True).report_action(preinscripcion)
                
        elif tipo == 'inscripcion':
            # Recuperar la inscripción específica
            inscripcion = request.env['admision.inscripcion'].sudo().search([
                ('id', '=', registro_id),
                ('aspirante_id', '=', aspirante.id)
            ], limit=1)
            
            if not inscripcion:
                return request.redirect('/mi/admision')
            
            return request.env.ref('admision.action_report_inscripcion').with_context(
                download=True).report_action(inscripcion)
                
        elif tipo == 'estudio' and values.get('is_estudiante'):
            # Generar constancia de estudio
            return request.env.ref('admision.action_report_constancia_estudio').with_context(
                download=True).report_action(aspirante)
        
        return request.redirect('/mi/admision')
    
    @http.route(['/verificar-aspirante'], type='json', auth="public", website=True)
    def verificar_aspirante(self, **kw):
        cedula = kw.get('cedula')
        
        if not cedula:
            return {'success': False, 'message': 'Debe proporcionar una cédula de identidad'}
        
        # Verificar formato de la cédula
        import re
        if not re.match(r'^[VE]-\d{5,10}$', cedula):
            return {'success': False, 'message': 'Formato de cédula inválido. Use V-XXXXXXXX o E-XXXXXXXX'}
        
        # Verificar si existe el aspirante
        aspirante = request.env['admision.aspirante'].sudo().search([('cedula', '=', cedula)], limit=1)
        
        if aspirante:
            return {
                'success': True,
                'exists': True,
                'tipo_asignacion': aspirante.tipo_asignacion,
                'state': aspirante.state,
                'programa': aspirante.programa_id.name if aspirante.programa_id else '',
                'sede': aspirante.sede_id.name if aspirante.sede_id else '',
            }
        else:
            return {
                'success': True,
                'exists': False,
            }