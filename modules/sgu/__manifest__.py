# -*- coding: utf-8 -*-
{
    'name': "Sistema de Gestión Universitaria (SGU)",
    'summary': """
        Módulo integrado para la gestión universitaria, incluyendo admisiones, carreras, sedes y procesos académicos.
    """,
    'description': """
        Este módulo implementa un sistema integral de gestión universitaria que permite:
        - Administrar instituciones, sedes y carreras
        - Gestionar periodos y procesos académicos
        - Administrar aspirantes y estudiantes
        - Procesar inscripciones directas
        - Gestionar horarios, secciones y pensums
    """,
    'author': "Desarrollo Odoo",
    'website': "http://www.example.com",
    'category': 'Education',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/sgu_security.xml',
        'security/ir.model.access.csv',
        'views/sgu_institucion_views.xml',
        'views/sgu_sede_views.xml',
        'views/sgu_nivel_academico_views.xml',
        'views/sgu_modalidad_views.xml',
        'views/sgu_area_views.xml',
        'views/sgu_carrera_views.xml',
        'views/sgu_periodo_views.xml',
        'views/sgu_proceso_views.xml',
        'views/sgu_pensum_views.xml',
        'views/sgu_autoridad_views.xml',
        'views/sgu_carrera_sede_views.xml',
        'views/sgu_horario_views.xml',
        'views/sgu_seccion_views.xml',
        'views/sgu_usuarios_views.xml',
        'views/sgu_aspirante_views.xml',

        'views/sgu_inscripcion_views.xml',
        'wizards/sgu_importar_opsu_wizard_views.xml',
        'wizards/sgu_importar_aprobados_wizard_views.xml',
        'reports/sgu_inscripcion_report.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
