{
    'name': 'Periodo Académico',
    'version': '1.0',
    'summary': 'Módulo para gestionar periodos académicos sin depender del website layout de Odoo',
    'description': """
        Permite registrar y gestionar periodos académicos utilizando el ORM de Odoo y una vista HTML
        personalizada, sin usar el layout del website.
    """,
    'category': 'Education',
    'author': 'Julian',
    'website': 'http://tusitio.com',
    'depends': ['base'],
    'data': [
         'views/periodo_academico_template.xml'
    ],
    'installable': True,
    'application': True,
}
