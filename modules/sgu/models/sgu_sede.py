# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import os

class Sede(models.Model):
    _name = 'sgu.sede'
    _description = 'Sede universitaria'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    codigo_sede = fields.Char('Código', required=True)
    direccion_sede = fields.Text('Dirección')
    correo_sede = fields.Char('Correo electrónico')
    telefono_sede = fields.Char('Teléfono')
    logo = fields.Binary('Logo')
    active = fields.Boolean('Activo', default=True)
    
    @api.model
    def _get_estados_selection(self):
        try:
            module_path = os.path.dirname(os.path.dirname(__file__))
            with open(os.path.join(module_path, 'data', 'venezuela.json'), 'r') as f:
                data = json.load(f)
            return [(str(e['id_estado']), e['estado']) for e in data]
        except Exception as e:
            return []

    @api.model
    def _get_municipios_selection(self):
        try:
            module_path = os.path.dirname(os.path.dirname(__file__))
            with open(os.path.join(module_path, 'data', 'venezuela.json'), 'r') as f:
                data = json.load(f)
            municipios = []
            for estado in data:
                for municipio in estado['municipios']:
                    municipios.append((f"{estado['id_estado']}_{municipio['municipio']}", 
                                    f"{estado['estado']} / {municipio['municipio']}"))
            return municipios
        except Exception as e:
            return []

    @api.model
    def _get_parroquias_selection(self):
        try:
            module_path = os.path.dirname(os.path.dirname(__file__))
            with open(os.path.join(module_path, 'data', 'venezuela.json'), 'r') as f:
                data = json.load(f)
            parroquias = []
            for estado in data:
                for municipio in estado['municipios']:
                    for parroquia in municipio['parroquias']:
                        parroquias.append((f"{estado['id_estado']}_{municipio['municipio']}_{parroquia}",
                                        f"{estado['estado']} / {municipio['municipio']} / {parroquia}"))
            return parroquias
        except Exception as e:
            return []

    estado_id = fields.Selection(selection='_get_estados_selection', string='Estado')
    municipio = fields.Selection(selection='_get_municipios_selection', string='Municipio')
    parroquia = fields.Selection(selection='_get_parroquias_selection', string='Parroquia')

    # Relaciones
    institucion_id = fields.Many2one('sgu.institucion', 'Institución', required=True)
    
    # Relación One2many al modelo pivot
    carrera_sede_ids = fields.One2many('sgu.carrera.sede', 'sede_id', string='Programas ofrecidos')
    
    # Campo computado para obtener solo las carreras
    carrera_ids = fields.Many2many('sgu.carrera', string='Carreras disponibles', compute='_compute_carrera_ids', store=False)
    
    def _compute_carrera_ids(self):
        for sede in self:
            sede.carrera_ids = sede.carrera_sede_ids.mapped('carrera_id')
