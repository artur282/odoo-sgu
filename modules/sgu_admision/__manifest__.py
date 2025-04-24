{
    'name': 'Sistema de Admisión SGU',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Gestión del proceso completo de admisión universitaria',
    'description': """
        Sistema de Admisión SGU
        ======================
        
        Este módulo gestiona el proceso completo de ingreso de nuevos estudiantes:
        * Recepción de listados oficiales (OPSU) y casos especiales
        * Preinscripción en línea
        * Inscripción formal
        * Conversión de aspirante a estudiante regular
    """,
    'author': 'Universidad Nacional Experimental de los Llanos Centrales Rómulo Gallegos',
    'website': 'https://www.unerg.edu.ve',
    'depends': ['base', 'mail', 'portal', 'web'],
    'data': [
        'security/admision_security.xml',
        'security/ir.model.access.csv',
        'data/admision_sequence.xml',
        'views/admision_proceso_views.xml',
        'views/admision_aspirante_views.xml',
        'views/admision_preinscripcion_views.xml',
        'views/admision_inscripcion_views.xml',
        'views/admision_programa_views.xml',
        'views/admision_sede_views.xml',
        'views/admision_seccion_views.xml',
        'views/admision_horario_views.xml',
        'views/admision_portal_templates.xml',
        'wizard/importar_opsu_view.xml',
        'wizard/importar_aprobados_view.xml',
        'views/admision_menu.xml',
        'reports/admision_reports.xml',
        'reports/constancia_preinscripcion_report.xml',
        'reports/constancia_inscripcion_report.xml',
    ],
    'demo': [
        'demo/admision_demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}