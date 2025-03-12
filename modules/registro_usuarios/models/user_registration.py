from odoo import models, fields

class UserRegistration(models.Model):
    _name = 'user.registration'
    _description = 'Registro de Usuarios'

    primer_nombre   = fields.Char(string="Primer Nombre", required=True)
    segundo_nombre  = fields.Char(string="Segundo Nombre", required=True)
    primer_apellido = fields.Char(string="Primer Apellido", required=True)
    segundo_apellido = fields.Char(string="Segundo Apellido", required=True)
    cedula          = fields.Integer(string="Cédula", required=True)
    correo          = fields.Char(string="Correo", required=True)
    genero          = fields.Selection([('hombre','Hombre'),
                                          ('mujer','Mujer')],
                                         string="Género", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    discapacidad     = fields.Selection([('ninguna', 'Ninguna'),
                                          ('diabetico', 'Soy diabetico'),
                                          ('paralitico', 'Soy paralitico')],
                                         string="Discapacidad", required=True, default='ninguna')
    etnia            = fields.Selection([('indio','Indio'),
                                          ('guajiro','Guajiro'),
                                          ('indu','Indu')],
                                         string="Etnia", required=True)
    telefono         = fields.Char(string="Teléfono", required=True)
    grupo_usuario    = fields.Selection([('superAdmin','Super Admin'),
                                          ('admin','Admin'),
                                          ('operador','Operador'),
                                          ('estudiante','Estudiante'),
                                          ('profesor','Profesor')],
                                         string="Grupo de Usuario", required=True)
