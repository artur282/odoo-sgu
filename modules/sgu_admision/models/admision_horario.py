# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AdmisionHorario(models.Model):
    _name = 'admision.horario'
    _description = 'Horario'
    _order = 'dia_semana, hora_inicio'
    
    name = fields.Char('Descripción', compute='_compute_name', store=True)
    seccion_id = fields.Many2one('admision.seccion', string='Sección', required=True)
    programa_id = fields.Many2one('admision.programa', related='seccion_id.programa_id', store=True)
    periodo_id = fields.Many2one('admision.periodo', related='seccion_id.periodo_id', store=True)
    
    # Información básica
    asignatura = fields.Char('Asignatura', required=True)
    profesor = fields.Char('Profesor', required=True)
    aula = fields.Char('Aula/Salón')
    
    # Horario
    dia_semana = fields.Selection([
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('7', 'Domingo')
    ], string='Día', required=True)
    
    hora_inicio = fields.Float('Hora Inicio', required=True, help="Formato 24 horas: 13.5 = 13:30")
    hora_fin = fields.Float('Hora Fin', required=True, help="Formato 24 horas: 15.5 = 15:30")
    duracion = fields.Float('Duración (Horas)', compute='_compute_duracion', store=True)
    
    active = fields.Boolean('Activo', default=True)
    
    @api.depends('asignatura', 'dia_semana', 'hora_inicio', 'hora_fin')
    def _compute_name(self):
        dias = {
            '1': 'Lunes', '2': 'Martes', '3': 'Miércoles', 
            '4': 'Jueves', '5': 'Viernes', '6': 'Sábado', '7': 'Domingo'
        }
        for record in self:
            hora_inicio_str = self._float_to_hora(record.hora_inicio)
            hora_fin_str = self._float_to_hora(record.hora_fin)
            dia = dias.get(record.dia_semana, '')
            record.name = f"{record.asignatura} - {dia} {hora_inicio_str}-{hora_fin_str}"
    
    @api.depends('hora_inicio', 'hora_fin')
    def _compute_duracion(self):
        for record in self:
            record.duracion = max(0, record.hora_fin - record.hora_inicio)
    
    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError(_("La hora de inicio debe ser anterior a la hora de fin."))
            
            if record.hora_inicio < 6.0 or record.hora_inicio > 22.0:
                raise ValidationError(_("La hora de inicio debe estar entre 6:00 y 22:00."))
            
            if record.hora_fin < 7.0 or record.hora_fin > 23.0:
                raise ValidationError(_("La hora de fin debe estar entre 7:00 y 23:00."))
    
    def _float_to_hora(self, tiempo_float):
        """Convierte un tiempo en formato float a string hh:mm"""
        horas = int(tiempo_float)
        minutos = int((tiempo_float - horas) * 60)
        return f"{horas:02d}:{minutos:02d}"
    
    @api.model
    def create(self, vals):
        # Verificar conflicto de horarios para la sección
        if vals.get('seccion_id') and vals.get('dia_semana') and 'hora_inicio' in vals and 'hora_fin' in vals:
            self._check_conflicto_horario(
                vals.get('seccion_id'),
                vals.get('dia_semana'),
                vals.get('hora_inicio'),
                vals.get('hora_fin')
            )
        
        return super(AdmisionHorario, self).create(vals)
    
    def write(self, vals):
        # Verificar conflicto de horarios si se modifican los campos relevantes
        for record in self:
            seccion_id = vals.get('seccion_id', record.seccion_id.id)
            dia_semana = vals.get('dia_semana', record.dia_semana)
            hora_inicio = vals.get('hora_inicio', record.hora_inicio)
            hora_fin = vals.get('hora_fin', record.hora_fin)
            
            self._check_conflicto_horario(seccion_id, dia_semana, hora_inicio, hora_fin, record.id)
        
        return super(AdmisionHorario, self).write(vals)
    
    def _check_conflicto_horario(self, seccion_id, dia_semana, hora_inicio, hora_fin, exclude_id=None):
        """Verifica si hay conflicto de horarios para una sección"""
        domain = [
            ('seccion_id', '=', seccion_id),
            ('dia_semana', '=', dia_semana),
            '|', 
                '&', ('hora_inicio', '<=', hora_inicio), ('hora_fin', '>', hora_inicio),
                '&', ('hora_inicio', '<', hora_fin), ('hora_fin', '>=', hora_fin)
        ]
        
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
        
        conflictos = self.search(domain)
        
        if conflictos:
            raise ValidationError(_(
                "Hay un conflicto de horario con la clase de %s programada en el mismo día y hora."
            ) % conflictos[0].asignatura)