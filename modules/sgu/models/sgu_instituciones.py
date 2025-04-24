from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Institucion(models.Model):
    _name = 'sgu_institucion'
    _description = 'Institución Universitaria'
    _rec_name = 'nombre_institucion'

    nombre_institucion = fields.Char(string='Nombre de la Institución', required=True, index=True)
    logo = fields.Binary(string='Logo', help="Logo de la institución (formato imagen)")
    codigo_institucion = fields.Integer(string='Código de la Institución', required=True)
    correo_institucion = fields.Char(string='Correo Electrónico')
    telefono_institucion = fields.Char(string='Teléfono')
    firma_rector = fields.Binary(string='Firma del Rector')
    firma_director = fields.Binary(string='Firma del Director de Control de Estudio')
    firma_secretaria = fields.Binary(string='Firma de la Secretaria')
    institutos_ids = fields.One2many('sgu_sedes', 'instituciones_id', string='Sedes')
    descripcion = fields.Html(string='Descripción')
    institutos_count = fields.Integer(string='Número de Institutos', compute='_compute_institutos_count')
    active = fields.Boolean(string="Activo", default=True)
    company_id = fields.Many2one('res.company', string='Compañía Relacionada', ondelete='cascade')

    _sql_constraints = [
        ('codigo_institucion_uniq', 'unique(codigo_institucion)', 'El código de la institución debe ser único.'),
        ('nombre_institucion_uniq', 'unique(nombre_institucion)', 'El nombre de la institución debe ser único.')
    ]

    @api.constrains('correo_institucion')
    def _check_correo_institucion(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            if record.correo_institucion and not re.match(email_regex, record.correo_institucion):
                raise ValidationError("El correo de la institución debe ser válido.")

    @api.depends('institutos_ids')
    def _compute_institutos_count(self):
        for record in self:
            record.institutos_count = len(record.institutos_ids)

    @api.model
    def create(self, vals):
        institucion = super().create(vals)
        if not institucion.company_id:
            institucion.company_id = self.env['res.company'].create({'name': institucion.nombre_institucion})
        return institucion

    def write(self, vals):
        res = super().write(vals)
        if 'nombre_institucion' in vals:
            for record in self:
                if record.company_id:
                    record.company_id.name = record.nombre_institucion
        return res

