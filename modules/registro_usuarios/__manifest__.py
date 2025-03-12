{
    "name": "Módulo Registro de Usuarios",
    "summary": "CRUD de registros de usuarios mediante rutas HTTP usando el ORM de Odoo.",
    "description": """
        Módulo para crear, leer, actualizar y eliminar registros de usuarios. 
        Se expone una interfaz vía rutas que muestra un formulario de registro 
        y un listado de usuarios registrados.
    """,
    "author": "Tu Nombre",
    "category": "Tools",
    "version": "0.1",
    "depends": ["base"],
    "data": [
        'views/user_registration_template.xml'
        # Puedes referenciar aquí archivos XML si en el futuro deseas agregar vistas, seguridad, etc.
    ],
    "installable": True,
    "application": True,
}
