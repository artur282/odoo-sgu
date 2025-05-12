# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Aspirante(models.Model):
    _name = 'sgu.aspirante'
    _description = 'Aspirante a ingreso'
    _rec_name = 'cedula'

    cedula = fields.Char('Cédula', required=True, tracking=True)
    codigo_opsu = fields.Char('Código OPSU', tracking=True)

    # Datos personales
    primer_nombre = fields.Char('Primer nombre', required=True)
    segundo_nombre = fields.Char('Segundo nombre')
    primer_apellido = fields.Char('Primer apellido', required=True)
    segundo_apellido = fields.Char('Segundo apellido')
    genero = fields.Selection([('hombre','Hombre'),
                              ('mujer','Mujer')],
                             string="Género", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    email = fields.Char('Correo electrónico')
    phone = fields.Char('Teléfono fijo')
    mobile = fields.Char('Teléfono móvil')

    # Datos adicionales
    discapacidad = fields.Boolean('Posee discapacidad')
    tipo_discapacidad = fields.Char('Tipo de discapacidad')
    etnia = fields.Selection([('ninguno','Ninguno'),
                             ('guajiro','Guajiro'),
                             ('wayuu', 'Wayuu'),
                             ('afrodescendiente', 'Afrodescendiente'),
                             ('indigena', 'Indígena'),
                             ('criollo', 'Criollo')],
                            string="Etnia", required=True)
    telefono = fields.Char(string="Teléfono", required=True)
    active = fields.Boolean(string="Activo", default=True)

    # Datos académicos
    tipo_asignacion = fields.Selection([
        ('opsu', 'OPSU'),
        ('rector', 'Rector'),
        ('secretaria', 'Secretaría'),
        ('dace', 'DACE'),
        ('aspirante', 'Aspirante a Cupo')
    ], string='Tipo de Asignación', required=True, default='aspirante', readonly=True)

    # Referencias a modelos base de SGU
    carrera_id = fields.Many2one('sgu.carrera', 'Programa/Carrera', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True)

    # Estado del aspirante
    state = fields.Selection([
        ('registrado', 'Registrado'),
        ('inscrito', 'Inscrito'),
        ('estudiante', 'Estudiante')
    ], string='Estado', default='registrado', tracking=True)

    # Relaciones
    inscripcion_ids = fields.One2many('sgu.inscripcion', 'aspirante_id', 'Inscripciones')

    # Datos complementarios
    direccion_completa = fields.Text('Dirección completa')
    contacto_emergencia = fields.Char('Contacto de emergencia')
    
    # Restricción de unicidad para la cédula
    _sql_constraints = [
        ('cedula_unique', 'unique(cedula)', 
         'Ya existe un aspirante con esta cédula')
    ]
    

    @api.onchange('inscripcion_ids')
    def _onchange_inscripciones(self):
        """Actualiza el estado cuando tiene inscripciones confirmadas"""
        if self.inscripcion_ids and any(i.state == 'confirmed' for i in self.inscripcion_ids):
            self.state = 'inscrito'
    
    def crear_estudiante(self):
        """Convertir aspirante en estudiante"""
        self.ensure_one()
        if self.state == 'inscrito':
            # Crear usuario estudiante
            vals = {
                'primer_nombre': self.primer_nombre,
                'segundo_nombre': self.segundo_nombre,
                'primer_apellido': self.primer_apellido,
                'segundo_apellido': self.segundo_apellido,
                'cedula': self.cedula,
                'sexo': 'M' if self.genero == 'hombre' else 'F',
                'fecha_nacimiento': self.fecha_nacimiento,
                'etnia': self.etnia,
                'telefono': self.telefono or self.mobile,
                'rol': 'estudiante',
                'email': self.email
            }
            estudiante = self.env['sgu.usuarios'].create(vals)
            self.state = 'estudiante'
            return {
                'name': 'Estudiante Creado',
                'type': 'ir.actions.act_window',
                'res_model': 'sgu.usuarios',
                'res_id': estudiante.id,
                'view_mode': 'form',
                'target': 'current',
            }
