# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Institucion(models.Model):
    _name = 'sgu.institucion'
    _description = 'Institución educativa'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    codigo = fields.Char('Código', required=True)
    direccion = fields.Text('Dirección')
    telefono = fields.Char('Teléfono')
    email = fields.Char('Correo electrónico')
    descripcion = fields.Html(string='Descripción')
    logo = fields.Binary('Logo')
    active = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one('res.company', 'Compañía', default=lambda self: self.env.company)

    # Relaciones
    sede_ids = fields.One2many('sgu.sede', 'institucion_id', 'Sedes')

    # se actualiza el nombre de la compañía asociada
    def write(self, vals):
        res = super().write(vals)
        if 'name' in vals:
            for record in self:
                if record.company_id:
                    record.company_id.name = record.name
        return res
