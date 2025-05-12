# -*- coding: utf-8 -*-

import base64
import csv
import io
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ImportarOpsuWizard(models.TransientModel):
    _name = 'sgu.importar.opsu.wizard'
    _description = 'Importar listado OPSU'

    archivo_csv = fields.Binary('Archivo CSV', required=True)
    archivo_nombre = fields.Char('Nombre del archivo')

    # Campos de mapeo para CSV
    campo_cedula = fields.Char('Campo de cédula', default='cedula')
    campo_nombre1 = fields.Char('Campo de primer nombre', default='primer_nombre')
    campo_nombre2 = fields.Char('Campo de segundo nombre', default='segundo_nombre')
    campo_apellido1 = fields.Char('Campo de primer apellido', default='primer_apellido')
    campo_apellido2 = fields.Char('Campo de segundo apellido', default='segundo_apellido')
    campo_carrera = fields.Char('Campo de carrera', default='carrera')
    campo_sede = fields.Char('Campo de sede', default='sede')
    campo_codigo_opsu = fields.Char('Campo de código OPSU', default='codigo_opsu')
    campo_genero = fields.Char('Campo de género', default='genero')
    
    def action_importar(self):
        """Importar datos de OPSU desde un archivo CSV"""
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
            self.campo_apellido1,
            self.campo_carrera,
            self.campo_sede,
            self.campo_codigo_opsu
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

                # Buscar carrera y sede
                carrera_val = row.get(self.campo_carrera, '')
                sede_val = row.get(self.campo_sede, '')
                if not carrera_val or not sede_val:
                    errores += 1
                    continue
                carreras = carrera_obj.search([('name', 'ilike', carrera_val)])
                if not carreras:
                    carreras = carrera_obj.search([('codigo', '=', carrera_val)])
                if not carreras:
                    errores += 1
                    continue
                sedes = sede_obj.search([('name', 'ilike', sede_val)])
                if not sedes:
                    sedes = sede_obj.search([('codigo_sede', '=', sede_val)])
                if not sedes:
                    errores += 1
                    continue
                carrera_id = carreras[0].id
                sede_id = sedes[0].id

                # Verificar si ya existe
                existe = aspirante_obj.search([('cedula', '=', cedula)])
                if existe:
                    existe.write({
                        'codigo_opsu': row.get(self.campo_codigo_opsu, ''),
                        'tipo_asignacion': 'opsu',
                        'carrera_id': carrera_id,
                        'sede_id': sede_id
                    })
                    aspirantes_creados += 1
                else:
                    genero_valor = row.get(self.campo_genero, '').lower()
                    genero = 'hombre' if genero_valor in ['m', 'h', 'hombre', 'masculino'] else 'mujer'
                    vals = {
                        'cedula': cedula,
                        'primer_nombre': row.get(self.campo_nombre1, ''),
                        'segundo_nombre': row.get(self.campo_nombre2, ''),
                        'primer_apellido': row.get(self.campo_apellido1, ''),
                        'segundo_apellido': row.get(self.campo_apellido2, ''),
                        'codigo_opsu': row.get(self.campo_codigo_opsu, ''),
                        'genero': genero,
                        'carrera_id': carrera_id,
                        'sede_id': sede_id,
                        'tipo_asignacion': 'opsu',
                        'etnia': 'ninguno',
                        'telefono': '',
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
