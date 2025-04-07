{
    'name': 'API Login',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Módulo para login mediante API externa',
    'description': 'Permite a los usuarios iniciar sesión utilizando una API externa.',
    'depends': ['base', 'website'],
    'data': [
        'views/login_api_template.xml',
        'views/protected_page_2.xml',
    ],
    'installable': True,
    'application': True,
}
