# -*- coding: utf-8 -*-
{
    'name': "sgu",

    'summary': "sistema de gestion universitaria",

    'description': """
modulo del sistema de gestion universitaria
    """,

    'author': "sgu unerg",
    'website': "",
    'category': 'tools',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [ 
        'security/ir.model.access.csv',
        'views/sgu_instituto_views.xml',
        'views/periodo_academico_template.xml',
        'views/user_registration_views.xml',
        'views/sgu_autoridad_views.xml',
        'views/sgu_carreras_views.xml',
        'views/sgu_areas_views.xml',
        'views/sgu_modalidad_views.xml',
        'views/sgu_nivel_academico_views.xml',
        'views/sgu_asignar_carrera_sede_views.xml',
        'views/pensum_views.xml',
        'views/admision.xml',
        'views/procesos.xml',
        'views/Asignacion_Procesos.xml',
        'views/sgu_sedes_views.xml',
        'views/sgu_menu.xml',
    ],
    'installable': True,
    'application': True,
}

