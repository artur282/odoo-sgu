# -*- coding: utf-8 -*-

import base64
import csv
import io
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ImportarAprobadosWizard(models.TransientModel):
    _name = 'sgu.importar.aprobados.wizard'
    _description = 'Importar casos aprobados'

    archivo_csv = fields.Binary('Archivo CSV', required=True)
    archivo_nombre = fields.Char('Nombre del archivo')
    tipo_aprobacion = fields.Selection([
        ('rector', 'Rector'),
        ('secretaria', 'Secretaría'),
        ('dace', 'DACE')
    ], string='Tipo de aprobación', required=True)
    carrera_id = fields.Many2one('sgu.carrera', 'Carrera por defecto', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede por defecto', required=True)
    
    # Campos de mapeo para CSV
    campo_cedula = fields.Char('Campo de cédula', default='cedula')
    campo_nombre1 = fields.Char('Campo de primer nombre', default='primer_nombre')
    campo_nombre2 = fields.Char('Campo de segundo nombre', default='segundo_nombre')
    campo_apellido1 = fields.Char('Campo de primer apellido', default='primer_apellido')
    campo_apellido2 = fields.Char('Campo de segundo apellido', default='segundo_apellido')
    campo_carrera = fields.Char('Campo de carrera', default='carrera')
    campo_sede = fields.Char('Campo de sede', default='sede')
    campo_genero = fields.Char('Campo de género', default='genero')
    campo_email = fields.Char('Campo de email', default='email')
    campo_telefono = fields.Char('Campo de teléfono', default='telefono')
    
    def action_importar(self):
        """Importar datos de casos aprobados desde un archivo CSV"""
        self.ensure_one()
        if not self.archivo_csv:
            raise UserError(_('Debe seleccionar un archivo para importar'))
        
        # Decodificar archivo
        csv_data = base64.b64decode(self.archivo_csv)
        csv_file = io.StringIO(csv_data.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        # Validar cabeceras requeridas
        cabeceras = reader.fieldnames
        required_fields = [
            self.campo_cedula, 
            self.campo_nombre1, 
            self.campo_apellido1
        ]
        
        for field in required_fields:
            if field not in (cabeceras or []):
                raise UserError(_(f'El archivo no contiene la columna requerida: {field}'))
        
        aspirantes_creados = 0
        errores = 0
        
        # Crear aspirantes
        aspirante_obj = self.env['sgu.aspirante']
        carrera_obj = self.env['sgu.carrera']
        sede_obj = self.env['sgu.sede']
        
        for row in reader:
            try:
                cedula = row.get(self.campo_cedula)
                if not cedula:
                    errores += 1
                    continue
                
                # Verificar si ya existe
                existe = aspirante_obj.search([('cedula', '=', cedula)])
                
                # Buscar carrera y sede si están especificadas en el CSV
                carrera_id = self.carrera_id.id
                sede_id = self.sede_id.id
                
                if (cabeceras and self.campo_carrera in cabeceras) and row.get(self.campo_carrera):
                    carreras = carrera_obj.search([
                        '|',
                        ('name', 'ilike', row[self.campo_carrera]),
                        ('codigo', '=', row[self.campo_carrera])
                    ])
                    if carreras:
                        carrera_id = carreras[0].id
                
                if (cabeceras and self.campo_sede in cabeceras) and row.get(self.campo_sede):
                    sedes = sede_obj.search([
                        '|',
                        ('name', 'ilike', row[self.campo_sede]),
                        ('codigo_sede', '=', row[self.campo_sede])
                    ])
                    if sedes:
                        sede_id = sedes[0].id
                
                if existe:
                    # Actualizar datos en lugar de crear uno nuevo
                    existe.write({
                        'tipo_asignacion': self.tipo_aprobacion,
                        'carrera_id': carrera_id,
                        'sede_id': sede_id
                    })
                    aspirantes_creados += 1
                else:
                    # Crear nuevo aspirante
                    genero_valor = row.get(self.campo_genero, '').lower()
                    genero = 'hombre' if genero_valor in ['m', 'h', 'hombre', 'masculino'] else 'mujer'
                    
                    vals = {
                        'cedula': cedula,
                        'primer_nombre': row.get(self.campo_nombre1, ''),
                        'segundo_nombre': row.get(self.campo_nombre2, ''),
                        'primer_apellido': row.get(self.campo_apellido1, ''),
                        'segundo_apellido': row.get(self.campo_apellido2, ''),
                        'genero': genero,
                        'carrera_id': carrera_id,
                        'sede_id': sede_id,
                        'tipo_asignacion': self.tipo_aprobacion,
                        'etnia': 'ninguno',
                        'telefono': row.get(self.campo_telefono, ''),
                        'email': row.get(self.campo_email, ''),
                        'fecha_nacimiento': fields.Date.today()  # Valor temporal
                    }
                    aspirante_obj.create(vals)
                    aspirantes_creados += 1
            except Exception as e:
                errores += 1
                
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Importación completada'),
                'message': _(f'Se procesaron {aspirantes_creados} registros con {errores} errores'),
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }
