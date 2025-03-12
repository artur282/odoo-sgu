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
        'views/sgu_autoridad_views.xml',
        'views/sgu_instituto_views.xml',
        'views/sgu_carreras_views.xml',
        'views/sgu_menu.xml',
    ],
    'installable': True,
    'application': True,
}

