from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PeriodoA(models.Model):
    _name = 'prueba1.periodoa'
    _description = 'tabla de manejo de periodos academicos'

    anio = fields.Integer(string='Año', required=True)
    periodo = fields.Selection([
        ('I','I'),
        ('II','II'),
        ('III','III')],
        string='Periodo', required=True)
    estado = fields.Boolean(string='Estado', default=False)  # Changed to Boolean field
    modalidad = fields.Selection([
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ], string='Modalidad', required=True)

    @api.constrains('anio')
    def _check_anio_range(self):
        for record in self:
            if record.anio < 1900 or record.anio > 2100:
                raise ValidationError("El año debe estar entre 1900 y 2100.")

    @api.onchange('modalidad')
    def _onchange_modalidad(self):
        if self.modalidad == 'anual':
            self.periodo = 'I'
            return {'domain': {'periodo': [('name', '=', 'I')]}}
        else:
            return {'domain': {'periodo': []}}

    @api.constrains('estado', 'modalidad')
    def _check_only_one_active_period(self):
        for record in self:
            if record.estado:
                existing_active_period = self.search([
                    ('modalidad', '=', record.modalidad),
                    ('estado', '=', True),
                    ('id', '!=', record.id)  # Exclude the current record
                ])
                if existing_active_period:
                    modalidad_label = dict(self.fields_get(['modalidad'])['modalidad']['selection']).get(record.modalidad)
                    raise ValidationError(f"Ya existe un periodo activo para la modalidad: {modalidad_label}")
    
    @api.constrains('anio', 'periodo', 'modalidad')
    def _check_unique_periodo(self):
        for record in self:
            existing_period = self.search([
                ('anio', '=', record.anio),
                ('periodo', '=', record.periodo),
                ('modalidad', '=', record.modalidad),
                ('id', '!=', record.id) 
            ])
            if existing_period:
                raise ValidationError("Ya existe un año con el mismo periodo y modalidad.")

class Procesos(models.Model):
    _name = 'prueba1.procesos'
    _description = 'tabla de creacion de procesos academicos'
    
    proceso = fields.Char(string='Proceso', required=True)

    @api.constrains('proceso')
    def _check_Existance(self):
        for record in self:
            existing_proceso = self.search([
                ('proceso', '=', record.proceso),
                ('id', '!=', record.id)  
            ])
            if existing_proceso:
                raise ValidationError("Ya existe un proceso con el mismo nombre.")

#class AProcesos(models.Model):
#    _name = 'prueba1.asigacionprocesos'
#    _description = 'tabla de asignacion de procesos academicos'
#    
#    proceso_id = fields.Many2one('prueba1.periodoa', string='Proceso', required=True)
#    carrera_id = fields.Many2one('prueba1.carrera', string='Carrera', required=True)
#    fecha_inicio = fields.Date(string='Fecha de Inicio', required=True)
#    fecha_fin = fields.Date(string='Fecha de Fin', required=True)
#    periodo_id = fields.Many2one('prueba1.periodoa', string='Periodo', required=True)

#    @api.constrains('fecha_inicio', 'fecha_fin')
#    def _check_fecha_inicio_fin(self):
#        for record in self:
#           if record.fecha_inicio > record.fecha_fin:
#               raise ValidationError("La fecha de inicio no puede ser mayor que la fecha de fin.")