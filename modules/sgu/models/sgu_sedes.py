from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Sedes(models.Model):
    _name = 'sgu_sedes'
    _description = 'Sedes de la institución'
    _rec_name = 'nombre_sedes'


    instituciones_id = fields.Many2one('sgu_institucion', string='Institución', required=True, ondelete='cascade', index=True)
    codigo_sede = fields.Integer(string='Código de la sede', required=True)
    nombre_sedes = fields.Char(string='Nombre de la sede', required=True, index=True)
    carreras_ids = fields.One2many('sgu_carreras', 'sede', string='Carreras')
    

    ESTADOS_VENEZUELA = [
        ('AM', 'Amazonas'),
        ('AN', 'Anzoátegui'),
        ('AP', 'Apure'),
        ('AR', 'Aragua'),
        ('BA', 'Barinas'),
        ('BO', 'Bolívar'),
        ('CA', 'Carabobo'),
        ('CO', 'Cojedes'),
        ('DA', 'Delta Amacuro'),
        ('DC', 'Distrito Capital'),
        ('FA', 'Falcón'),
        ('GU', 'Guárico'),
        ('LA', 'Lara'),
        ('ME', 'Mérida'),
        ('MI', 'Miranda'),
        ('MO', 'Monagas'),
        ('NE', 'Nueva Esparta'),
        ('PO', 'Portuguesa'),
        ('SU', 'Sucre'),
        ('TA', 'Táchira'),
        ('TR', 'Trujillo'),
        ('VA', 'La Guaira'),
        ('YA', 'Yaracuy'),
        ('ZU', 'Zulia'),
    ]
    
    estado_id = fields.Selection(
        selection=ESTADOS_VENEZUELA,
        string='Estado',
        required=True,
        help="Seleccione el estado de Venezuela donde se encuentra la institución."
    )
    municipio = fields.Char(string='Municipio')
    parroquia = fields.Char(string='Parroquia')
    direccion = fields.Char(string='Dirección')
    correo_sede = fields.Char(string='Correo Electrónico')
    telefono_sede = fields.Char(string='Teléfono')
    
    firma_coordinador = fields.Binary(string='Firma del Coordinador DACE Sectorial')
    logo = fields.Binary(string='Logo de la Sede')
    active = fields.Boolean(string="Activo", default=True)

    # Restricciones y validaciones
    @api.constrains('codigo_sede')
    def _check_codigo_sede(self):
        for record in self:
            if record.codigo_sede <= 0:
                raise ValidationError("El código de la sede debe ser un número positivo.")

    @api.constrains('correo_sede')
    def _check_correo_sede(self):
        for record in self:
            if record.correo_sede and '@' not in record.correo_sede:
                raise ValidationError("El correo de la sede debe ser válido.")

    @api.constrains('telefono_sede')
    def _check_telefono_sede(self):
        for record in self:
            if record.telefono_sede and not record.telefono_sede.isdigit():
                raise ValidationError("El teléfono de la sede debe contener solo números.")

