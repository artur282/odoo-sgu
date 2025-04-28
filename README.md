# Odoo SGU - Sistema de Gestión Universitaria

![Versión](https://img.shields.io/badge/Odoo-18.0-brightgreen)
![Estado](https://img.shields.io/badge/Estado-Desarrollo-blue)
![Licencia](https://img.shields.io/badge/Licencia-LGPL--3-orange)

> Sistema de gestión Universitaria para instituciones educativas de nivel superior basado en Odoo 18.0

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características Principales](#características-principales)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución del Servidor](#ejecución-del-servidor)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Desarrollo de Módulos](#desarrollo-de-módulos)
- [Solución de Problemas](#solución-de-problemas)
- [Contribución](#contribución)
- [Soporte](#soporte)
- [Licencia](#licencia)

## 📝 Descripción

Este sistema representa una implementación personalizada de Odoo 18.0 específicamente adaptada para la gestión académica y administrativa de instituciones educativas de nivel superior. El SGU integra procesos de gestión académica, administrativa y de personal en una plataforma única y centralizada.

## ✨ Características Principales

- **Gestión Académica**: Planes de estudio, asignaturas, calificaciones, horarios
- **Administración de Estudiantes**: Expedientes, seguimiento académico, proceso de admisión
- **Gestión de Personal**: Docentes, administrativos, evaluaciones
- **Portal Web**: Acceso para estudiantes, profesores y personal administrativo
- **Reportes**: Generación de informes académicos y administrativos personalizados

## 🔧 Requisitos del Sistema

### Hardware Recomendado

- **Procesador**: 4 núcleos o superior
- **Memoria RAM**: 8GB mínimo, 16GB recomendado
- **Almacenamiento**: SSD con al menos 20GB de espacio libre
- **Conexión a internet**: Requerida para actualizaciones y características en línea

### Software Necesario

- **Sistema Operativo**: Linux (recomendado), Windows 10/11, macOS
- **Python**: Versión 3.11 o superior
- **PostgreSQL**: Versión 12.0 o superior
- **Navegador Web**: Chrome, Firefox o Edge actualizado
- **Dependencias**: Listadas en `requirements.txt`

## 🚀 Instalación

### 1. Preparación del Entorno

#### 1.1 Instalar PostgreSQL

```bash
# En sistemas basados en Debian/Ubuntu
sudo apt update
sudo apt install postgresql postgresql-client

# Crear usuario y base de datos
sudo -u postgres createuser --createdb --pwprompt admin
sudo -u postgres createdb --owner=admin odoo
```

#### 1.2 Crear entorno virtual con Python 3.11

```bash
# Instalar venv si no está disponible
sudo apt install python3.11-venv

# Crear y activar entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

### 2. Clonar el Repositorio e Instalar Dependencias

```bash
git clone https://[url-del-repositorio]/odoo-sgu.git
cd odoo-sgu
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

### 3. Configuración de la Base de Datos

El archivo `odoo.conf` contiene la configuración básica. Modifícalo según tu entorno:

```ini
[options]
db_host = localhost
db_port = 5432
db_user = admin
db_password = 123
addons_path = addons,modules
db_name = odoo
http_interface = 0.0.0.0
http_port = 8069
admin_passwd = admin_secure_password
log_level = info
log_handler = [':INFO']
```

## ▶️ Ejecución del Servidor

### Iniciar el servidor Odoo en modo desarrollo

```bash
# Asegúrate de que el entorno virtual está activado
./odoo-bin -c odoo.conf --dev=all
```

### Iniciar el servidor en modo producción

```bash
./odoo-bin -c odoo.conf --no-http --workers=4
```

### Opciones de línea de comando útiles

- `--test-enable`: Habilita las pruebas automáticas
- `--db-filter=^mydb$`: Filtra las bases de datos disponibles
- `--limit-memory-soft`: Límite de memoria suave (en bytes)
- `--limit-time-cpu`: Límite de tiempo de CPU (en segundos)

### Acceso a la aplicación

Una vez iniciado el servidor, puedes acceder a la aplicación a través de:

- **URL**: <http://localhost:8069>
- **Credenciales por defecto**:
  - Usuario: admin
  - Contraseña: admin

## 📁 Estructura del Proyecto

```
odoo-18.0/
├── addons/                # Módulos oficiales de Odoo
├── modules/               # Módulos personalizados del SGU
├── odoo/                  # Código fuente principal de Odoo
├── configuracion/         # Archivos de configuración adicionales
├── odoo-bin               # Ejecutable principal
├── odoo.conf              # Configuración por defecto
└── requirements.txt       # Dependencias Python
```

## 💻 Desarrollo de Módulos

### Crear un nuevo módulo

1. Estructura básica de un módulo:

```
mi_modulo/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── controllers.py
├── models/
│   ├── __init__.py
│   └── models.py
├── views/
│   └── views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── static/
    └── description/
        └── icon.png
```

2. Ejemplo de archivo `__manifest__.py`:

```python
{
    'name': "Mi Módulo SGU",
    'summary': "Descripción corta del módulo",
    'description': """
        Descripción larga del módulo
        que puede tener varias líneas
    """,
    'author': "Tu Nombre",
    'website': "http://www.ejemplo.com",
    'category': 'SGU',
    'version': '1.0',
    'depends': ['base', 'sgu_academico'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
```

3. **Activar modo desarrollador**:
   - Accede a Odoo
   - Ve a Configuración > Activar modo desarrollador
   - Actualiza la lista de aplicaciones en Aplicaciones > Actualizar lista de aplicaciones
   - Busca e instala tu módulo

### Mejores prácticas

- Sigue las convenciones de código de Odoo
- Documenta tu código con docstrings
- Escribe tests para tus módulos
- Revisa los logs con `tail -f /var/log/odoo/odoo.log`

## ⚠️ Solución de Problemas

### Problemas comunes y soluciones

| Problema | Posible Solución |
|----------|------------------|
| Error de acceso a la base de datos | Verifica las credenciales en `odoo.conf` y los permisos de PostgreSQL |
| Módulo no aparece | Revisa que esté incluido en `addons_path` y actualiza la lista de aplicaciones |
| Error de Python | Verifica que todas las dependencias están instaladas correctamente |
| Lentitud en el sistema | Ajusta los parámetros de workers y límites de memoria en la configuración |
| Error de permisos | Verifica los permisos de usuario en el sistema y en la base de datos |

### Verificar logs

```bash
tail -f /var/log/odoo/odoo.log
```

## 📄 Licencia

Este proyecto está bajo la licencia LGPL-3. Consulta el archivo `LICENSE` para más detalles.

---
© 2025 Sistema de Gestión Universitaria. Todos los derechos reservados.
