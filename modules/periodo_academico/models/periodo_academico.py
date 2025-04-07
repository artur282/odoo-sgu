from odoo import models, fields

class PeriodoAcademico(models.Model):
    _name = 'periodo.academico'
    _description = 'Periodo Académico'

    ano = fields.Integer(string='Año', required=True)
    tipo = fields.Selection([
         ('Semestral', 'Semestral'),
         ('Anual', 'Anual'),
         ('Trimestral', 'Trimestral')
    ], string='Tipo', required=True)
    periodo = fields.Selection([
         ('I', 'I'),
         ('II', 'II'),
         ('III', 'III')
    ], string='Periodo', required=True)
    status = fields.Selection([
         ('Activo', 'Activo'),
         ('Inactivo', 'Inactivo')
    ], string='Status', required=True, default='Inactivo')

    def cambiar_status(self):
        for record in self:
            record.status = 'Inactivo' if record.status == 'Activo' else 'Activo'
