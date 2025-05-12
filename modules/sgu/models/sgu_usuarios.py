# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Usuarios(models.Model):
    _name = 'sgu.usuarios'
    _description = 'Registro de Usuarios'
    _rec_name = 'cedula'

    primer_nombre = fields.Char(string="Primer Nombre", required=True)
    segundo_nombre = fields.Char(string="Segundo Nombre", required=False)
    primer_apellido = fields.Char(string="Primer Apellido", required=True)
    segundo_apellido = fields.Char(string="Segundo Apellido", required=False)
    cedula = fields.Char(string="Cédula de identidad", required=True)
    sexo = fields.Selection([("M","Masculino"),("F","Femenino")], string="Sexo", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento", required=True)
    etnia = fields.Selection([("ninguno","Ninguno"),
                            ("criollo","Criollo"),
                            ("afrodescendiente","Afrodescendiente"),
                            ("indigena","Indigena"),
                            ('wayuu','Wayuu'),
                            ('guajiro','Guajiro')],
                            string="Etnia", required=True)
    telefono = fields.Char(string="Teléfono")
    # Campo para definir el rol del usuario según el documento aprobado
    rol = fields.Selection([
        ('super_usuario', 'Super Usuario'),  # Gestión total del módulo, creación de usuarios, asignación de privilegios, procesos
        ('usuario_admin', 'Usuario Admin'),  # Asignación de privilegios a usuarios sectoriales
        ('operador_admin', 'Operador Admin'),  # Consultar admitidos OPSU, realizar inscripciones, generar reportes
        ('estudiante', 'Estudiante'),  # Actualizar datos, consultar horario, descargar constancias
    ], string="Rol del Usuario", required=True)
    active = fields.Boolean(string="Activo", default=True)
    
    # Campos adicionales
    email = fields.Char(string="Correo electrónico")
    direccion = fields.Text(string="Dirección")
    user_id = fields.Many2one('res.users', string='Usuario del sistema')
    
    # Restricción de unicidad para la cédula
    _sql_constraints = [
        ('cedula_unique', 'unique(cedula)', 
         'Ya existe un usuario con esta cédula')
    ]
    
    def crear_usuario_sistema(self):
        """Crear un usuario del sistema asociado a este usuario SGU"""
        for record in self:
            if not record.user_id:
                # Crear grupo según rol si no existe
                user_vals = {
                    'name': f"{record.primer_nombre} {record.primer_apellido}",
                    'login': record.cedula,
                    'email': record.email,
                    'groups_id': [(4, self.env.ref('base.group_user').id)]
                }
                # Agregar grupos específicos según rol
                if record.rol == 'super_usuario':
                    user_vals['groups_id'].append((4, self.env.ref('base.group_system').id))
                
                user = self.env['res.users'].create(user_vals)
                record.user_id = user.id
