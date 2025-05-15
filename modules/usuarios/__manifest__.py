{
    'name': 'Gestión de Usuarios Web',
    'version': '1.0',
    'category': 'Education',
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'license': 'LGPL-3',
    'summary': 'Módulo completo para gestión de usuarios en entornos educativos',
    'description': """
        Módulo para administración de usuarios, grupos y control de accesos
        en sistemas educativos. Incluye:
        - Gestión de perfiles de usuario
        - Control de permisos
        - Grupos personalizados
        - Sistema de autenticación extendido
    """, 
    'depends': ['base','web','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/gestion_usuarios_views.xml',
        # 'demo/demo_data.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'usuarios/static/src/css/usuario_styles.scss',
        ],
    },
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
