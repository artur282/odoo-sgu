from odoo import models, fields, api

class Usuario(models.Model):
    _name = 'gestion.usuarios'
    _description = 'Usuarios'
    _inherit = ['mail.thread']

    name = fields.Char(string="Nombre Completo", compute='_compute_full_name', store=True, track_visibility='onchange')
    email = fields.Char(string="Correo Electrónico", required=True, track_visibility='onchange')
    group_ids = fields.Many2many(
        'gestion.grupos', 
        string="Grupos de Usuario",
        relation='usuario_grupo_rel',
        column1='usuario_id',
        column2='grupo_id'
    )
    is_system_user = fields.Boolean(string="Es usuario del sistema", default=False, track_visibility='onchange')
    image_1920 = fields.Binary("Imagen de Perfil", attachment=True)
    image_128 = fields.Binary("Miniatura", related="image_1920", store=False, readonly=True)

    cedula = fields.Char(string="Cédula", required=True, size=10, track_visibility='onchange')
    primer_apellido = fields.Char(string="Primer Apellido", required=True, track_visibility='onchange')
    segundo_apellido = fields.Char(string="Segundo Apellido", track_visibility='onchange')
    primer_nombre = fields.Char(string="Primer Nombre", required=True, track_visibility='onchange')
    segundo_nombre = fields.Char(string="Segundo Nombre", track_visibility='onchange')
    sexo = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro')
    ], string="Sexo", track_visibility='onchange')
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", track_visibility='onchange')
    discapacidad = fields.Boolean(string="Tiene Discapacidad", track_visibility='onchange')
    etnia = fields.Selection([
        ('mestizo', 'Mestizo'),
        ('afro', 'Afrodescendiente'),
        ('indigena', 'Indígena'),
        ('montubio', 'Montubio'),
        ('blanco', 'Blanco'),
        ('otro', 'Otro')
    ], string="Etnia", track_visibility='onchange')
    telefono_l = fields.Char(string="Teléfono Fijo", track_visibility='onchange')
    telefono_m = fields.Char(string="Teléfono Móvil", required=True, track_visibility='onchange')
    status = fields.Boolean(string="Activo", default=True, track_visibility='onchange')

    @api.depends('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido')
    def _compute_full_name(self):
        for record in self:
            record.name = " ".join(filter(None, [
                record.primer_nombre,
                record.segundo_nombre,
                record.primer_apellido,
                record.segundo_apellido
            ]))


class GrupoUsuario(models.Model):
    _name = 'gestion.grupos'
    _description = 'Grupos de Usuarios'

    name = fields.Char(string="Nombre del Grupo", required=True)
    description = fields.Text(string="Descripción")
    color = fields.Integer(string="Color Index")


class ControlAcceso(models.Model):
    _name = 'gestion.acceso.control'
    _description = 'Control de Acceso de Usuarios'

    usuario_id = fields.Many2one('gestion.usuarios', string="Usuario", required=True)
    grupo_ids = fields.Many2many(
        'gestion.grupos',
        string="Grupos de Usuario",
        relation='control_acceso_grupo_rel',
        column1='control_acceso_id',
        column2='grupo_id'
    )
    permiso_ids = fields.Many2many(
        'ir.model.access',
        string="Permisos",
        relation='control_acceso_permiso_rel',
        column1='control_acceso_id',
        column2='permiso_id'
    )
