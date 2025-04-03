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

    firma_rector = fields.Binary(string='Firma del Rector', help="Firma del rector (formato imagen)")
    firma_director = fields.Binary(string='Firma del Director de Control de Estudio', help="Firma del director de control de estudio (formato imagen)")
    firma_secretaria = fields.Binary(string='Firma de la Secretaria', help="Firma de la secretaria (formato imagen)")

    institutos_ids = fields.One2many('sgu_sedes', 'instituciones_id', string='Sedes')
    descripcion = fields.Html(string='Descripción')
    institutos_count = fields.Integer(string='Número de Institutos', compute='_compute_institutos_count')
    active = fields.Boolean(string="Activo", default=True)

    # Restricciones y validaciones
    _sql_constraints = [
        ('codigo_institucion_uniq', 'unique(codigo_institucion)', 'El código de la institución debe ser único.'),
        ('nombre_institucion_uniq', 'unique(nombre_institucion)', 'El nombre de la institución debe ser único.')
    ]

    @api.constrains('codigo_institucion')
    def _check_codigo_institucion(self):
        for record in self:
            if record.codigo_institucion <= 0:
                raise ValidationError("El código de la institución debe ser un número positivo.")

    

    @api.constrains('correo_institucion')
    def _check_correo_institucion(self):
        for record in self:
            if record.correo_institucion:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.correo_institucion):
                    raise ValidationError("El correo de la institución debe ser válido.")

    @api.constrains('telefono_institucion')
    def _check_telefono_institucion(self):
        for record in self:
            if record.telefono_institucion and not record.telefono_institucion.isdigit():
                raise ValidationError("El teléfono de la institución debe contener solo números.")

    # Creación y actualización de registros
    # @api.model
    # def create(self, vals):
    #     company = self.env['res.company'].create({
    #         'name': vals['nombre_institucion'],
    #         'logo': vals.get('logo'),
    #         'city': vals.get('ciudad'),
    #         'state_id': vals.get('estado_id'),
    #         'country_id': vals.get('pais_id'),
    #         'email': vals.get('correo_institucion'),
    #         'phone': vals.get('telefono_institucion')
    #     })
    #     vals['company_id'] = company.id
    #     partner = self.env['res.partner'].create({
    #         'name': vals.get('nombre_institucion', 'Institución'),
    #     })
    #     vals['partner_id'] = partner.id
    #     return super(Institucion, self).create(vals)

    # def write(self, vals):
    #     if 'nombre_institucion' in vals or 'logo' in vals or 'ciudad' in vals or 'estado_id' in vals or 'pais_id' in vals or 'correo_institucion' in vals or 'telefono_institucion' in vals:
    #         company_vals = {
    #             'name': vals.get('nombre_institucion', self.company_id.name),
    #             'logo': vals.get('logo', self.company_id.logo),
    #             'city': vals.get('ciudad', self.company_id.city),
    #             'state_id': vals.get('estado_id', self.company_id.state_id.id),
    #             'country_id': vals.get('pais_id', self.company_id.country_id.id),
    #             'email': vals.get('correo_institucion', self.company_id.email),
    #             'phone': vals.get('telefono_institucion', self.company_id.phone)
    #         }
    #         self.company_id.write(company_vals)
    #         partner_vals = {
    #             'name': vals.get('nombre_institucion', self.partner_id.name),
    #         }
    #         self.partner_id.write(partner_vals)
    #     return super(Institucion, self).write(vals)

    # def unlink(self):
    #     self.company_id.unlink()
    #     self.partner_id.unlink()
    #     return super(Institucion, self).unlink()

    # Métodos de acciones
    def crear_instituto(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Crear Instituto',
            'res_model': 'sgu_instituto',
            'view_mode': 'form',
            'context': {'default_institucion_id': self.id, 'default_company_id': self.company_id.id},
        }
        return action

    def ver_institutos(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Institutos',
            'res_model': 'sgu_instituto',
            'view_mode': 'list,form',
            'views': [
                (self.env.ref('sgu_institucion.view_instituto_list').id, 'list'),
                (self.env.ref('sgu_institucion.view_instituto_form').id, 'form'),
            ],
            'domain': [('institucion_id', '=', self.id)],
        }
        return action

    # Método computado
    @api.depends('institutos_ids')
    def _compute_institutos_count(self):
        for record in self:
            record.institutos_count = len(record.institutos_ids)

