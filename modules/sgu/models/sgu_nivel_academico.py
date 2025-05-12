# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NivelAcademico(models.Model):
    _name = 'sgu.nivel.academico'
    _description = 'Nivel académico de la carrera (licenciatura, maestría, doctorado)'
    _rec_name = 'nivel'

    nivel = fields.Char('Nivel', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    carrera_ids = fields.One2many('sgu.carrera', 'nivel_academico_id', 'Carreras')
