from odoo import models, fields, api

class SguAreas(models.Model):
    _name = 'sgu_areas'
    _description = 'Áreas de la institución'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre', required=True)
    codigo = fields.Integer(string='Código', required=True)
    carrera_area = fields.One2many('sgu_carreras', 'area_carrera', string='Carreras')
    sede_id = fields.Many2one('sgu_sedes', string='Sede', ondelete='cascade')
    institucion_id = fields.Many2one('sgu_institucion', string='Institución', ondelete='cascade')
    active = fields.Boolean(string="Activo", default=True)
    logo = fields.Image(string="Logo")

    @api.onchange('carrera_area')
    def _onchange_carrera_area(self):
        if self.carrera_area:
            self.sede_id = self.carrera_area[0].sede_id if self.carrera_area[0].sede_id else False

    def toggle_active(self):
        for record in self:
            record.active = not record.active
