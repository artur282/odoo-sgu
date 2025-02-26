from odoo import models, fields

class SguAutoridad(models.Model):
    _name = 'sgu.autoridad'

    autoridades = fields.Char(string='Autoridades')
    autoriada = fields.Selection(
        selection='_get_autoridades',
        string='Autoriada'
    )
    institucion = fields.Char(string='Institución')
    nombre = fields.Char(string='Nombre')
    firmaDigital = fields.Image(string='Firma Digital')

    def _get_autoridades(self):
        autoridades_str = self.autoridades or ''
        autoridades_list = autoridades_str.split(',')
        return [(autoridad.strip(), autoridad.strip()) for autoridad in autoridades_list]

class SguCarreras(models.Model):
    _name = 'sgu.carreras'

    codigo = fields.Integer(string='Código')
    carrera = fields.Char(string='Carrera')
    modalidad = fields.Selection([
        ('anual', 'Anual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral')
    ], string='Modalidad')

class SguInstituto(models.Model):
    _name = 'sgu.instituto'

    codigo_opsu = fields.Integer(string='Código OPSU')
    nombre = fields.Char(string='Nombre')
    descripcion = fields.Text(string='Descripción')
    direccion = fields.Char(string='Dirección')
    telefono = fields.Integer(string='Teléfono')
    correo = fields.Char(string='Correo')