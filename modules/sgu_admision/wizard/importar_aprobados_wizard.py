# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import csv
import io
import logging

_logger = logging.getLogger(__name__)

class ImportarAprobadosWizard(models.TransientModel):
    _name = 'admision.importar.aprobados.wizard'
    _description = 'Importar Listado de Aprobados Especiales'
    
    archivo = fields.Binary('Archivo CSV', required=True, help="Archivo CSV con el listado de aprobados")
    archivo_nombre = fields.Char('Nombre del archivo')
    delimitador = fields.Char('Delimitador', default=',', help="Delimitador usado en el archivo CSV")
    
    tipo_aprobacion = fields.Selection([
        ('rector', 'Rector'),
        ('secretaria', 'Secretaria'),
        ('dace', 'DACE')
    ], string='Tipo de Aprobación', required=True, default='rector')
    
    def action_importar(self):
        if not self.archivo:
            raise UserError(_("Debe seleccionar un archivo"))
        
        try:
            # Decodificar archivo
            csv_data = base64.b64decode(self.archivo)
            file_input = io.StringIO(csv_data.decode('utf-8'))
            reader = csv.reader(file_input, delimiter=self.delimitador)
            
            # Saltarse la fila de encabezado
            header = next(reader, None)
            
            if not header:
                raise UserError(_("El archivo está vacío"))
            
            # Verificar que las columnas requeridas estén presentes
            required_columns = ['cedula', 'nombres', 'apellidos', 'programa', 'sede', 'codigo_opsu']
            found_columns = {col.lower(): i for i, col in enumerate(header)}
            
            missing_columns = []
            for col in required_columns:
                if col not in found_columns:
                    missing_columns.append(col)
            
            if missing_columns:
                raise UserError(_("Faltan columnas requeridas: %s") % 
                                ", ".join(missing_columns))
            
            # Procesar filas
            created = 0
            updated = 0
            errors = 0
            
            for row in reader:
                if not row or len(row) < len(header):
                    _logger.warning("Fila incompleta: %s", row)
                    errors += 1
                    continue
                
                try:
                    cedula = row[found_columns['cedula']].strip()
                    # Asegurarse de que la cédula tenga formato V-XXXXXXX o E-XXXXXXX
                    if not cedula.startswith('V-') and not cedula.startswith('E-'):
                        cedula = 'V-' + cedula
                    
                    nombres = row[found_columns['nombres']].strip()
                    apellidos = row[found_columns['apellidos']].strip()
                    programa_nombre = row[found_columns['programa']].strip()
                    sede_nombre = row[found_columns['sede']].strip()
                    
                    # Obtener código OPSU si existe en el CSV
                    codigo_opsu = None
                    if 'codigo_opsu' in found_columns and row[found_columns['codigo_opsu']]:
                        codigo_opsu = row[found_columns['codigo_opsu']].strip()
                    
                    # Buscar programa y sede
                    programa = self.env['admision.programa'].search([
                        ('name', '=ilike', programa_nombre)
                    ], limit=1)
                    
                    sede = self.env['admision.sede'].search([
                        ('name', '=ilike', sede_nombre)
                    ], limit=1)
                    
                    # Si no se encuentra programa o sede, crear mensaje de error
                    if not programa:
                        _logger.warning("Programa no encontrado: %s", programa_nombre)
                        errors += 1
                        continue
                    
                    if not sede:
                        _logger.warning("Sede no encontrada: %s", sede_nombre)
                        errors += 1
                        continue
                    
                    # Buscar si ya existe el aspirante
                    aspirante = self.env['admision.aspirante'].search([
                        ('cedula', '=', cedula)
                    ], limit=1)
                    
                    if aspirante:
                        # Actualizar aspirante existente
                        partner = aspirante.partner_id
                        partner.write({
                            'name': nombres + ' ' + apellidos,
                        })
                        
                        vals_update = {
                            'tipo_asignacion': self.tipo_aprobacion,
                            'programa_id': programa.id,
                            'sede_id': sede.id,
                        }
                        
                        # Añadir código OPSU si existe
                        if codigo_opsu:
                            vals_update['codigo_opsu'] = codigo_opsu
                            
                        aspirante.write(vals_update)
                        updated += 1
                    else:
                        # Crear nuevo partner y aspirante
                        partner = self.env['res.partner'].create({
                            'name': nombres + ' ' + apellidos,
                            'company_type': 'person',
                        })
                        
                        vals_create = {
                            'cedula': cedula,
                            'partner_id': partner.id,
                            'tipo_asignacion': self.tipo_aprobacion,
                            'programa_id': programa.id,
                            'sede_id': sede.id,
                            'state': 'registrado',
                        }
                        
                        # Añadir código OPSU si existe
                        if codigo_opsu:
                            vals_create['codigo_opsu'] = codigo_opsu
                            
                        self.env['admision.aspirante'].create(vals_create)
                        created += 1
                
                except Exception as e:
                    _logger.error("Error procesando fila: %s", e)
                    errors += 1
            
            # Mostrar resumen
            message = _(
                "Importación completada:\n"
                "- Aspirantes creados: %d\n"
                "- Aspirantes actualizados: %d\n"
                "- Errores: %d"
            ) % (created, updated, errors)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Resultado de la importación'),
                    'message': message,
                    'sticky': False,
                    'type': 'success' if errors == 0 else 'warning',
                }
            }
            
        except Exception as e:
            raise UserError(_("Error al procesar el archivo: %s") % str(e))