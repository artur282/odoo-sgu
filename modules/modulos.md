# 📘 Módulo Integrado SGU (Sistema de Gestión Universitaria)

## Introducción

Este documento describe la nueva estructura del módulo integrado SGU (Sistema de Gestión Universitaria), que combina las funcionalidades anteriormente divididas entre los módulos SGU y SGU_ADMISION. Esta integración elimina la duplicación de entidades y crea una arquitectura más clara y eficiente, facilitando el mantenimiento y mejorando la consistencia de los datos.

## Arquitectura propuesta

### Principio general

- **SGU**: Un único módulo integral que contiene todas las entidades y funcionalidades del sistema universitario, incluyendo los procesos de admisión

## Módulo SGU

### Modelos principales - Entidades fundamentales

#### 1. Instituciones (`sgu.institucion`)

```python
class Institucion(models.Model):
    _name = 'sgu.institucion'
    _description = 'Institución educativa'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    codigo = fields.Char('Código', required=True)
    direccion = fields.Text('Dirección')
    telefono = fields.Char('Teléfono')
    email = fields.Char('Correo electrónico')
    descripcion = fields.Html(string='Descripción')
    logo = fields.Binary('Logo')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    sede_ids = fields.One2many('sgu.sede', 'institucion_id', 'Sedes')

    # se actualiza el nombre de la compañía asociada
    def write(self, vals):
        res = super().write(vals)
        if 'nombre_institucion' in vals:
            for record in self:
                if record.company_id:
                    record.company_id.name = record.nombre_institucion
        return res
```

#### 2. Sedes (`sgu.sede`)

```python
class Sede(models.Model):
    _name = 'sgu.sede'
    _description = 'Sede universitaria'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    codigo_sede = fields.Integer('Código', required=True)
    direccion_sede = fields.Text('Dirección')
    correo_sede = fields.Char('Correo electrónico')
    telefono_sede = fields.Char('Teléfono')
    logo = fields.Binary('Logo')
    active = fields.Boolean('Activo', default=True)
        @api.model
    def _get_estados_selection(self):
        with open('venezuela.json', 'r') as f:
            data = json.load(f)
        return [(str(e['id_estado']), e['estado']) for e in data]

    @api.model
    def _get_municipios_selection(self):
        with open('venezuela.json', 'r') as f:
            data = json.load(f)
        municipios = []
        for estado in data:
            for municipio in estado['municipios']:
                municipios.append((f"{estado['id_estado']}_{municipio['municipio']}", 
                                f"{estado['estado']} / {municipio['municipio']}")
        return municipios

    @api.model
    def _get_parroquias_selection(self):
        with open('venezuela.json', 'r') as f:
            data = json.load(f)
        parroquias = []
        for estado in data:
            for municipio in estado['municipios']:
                for parroquia in municipio['parroquias']:
                    parroquias.append((f"{estado['id_estado']}_{municipio['municipio']}_{parroquia}",
                                    f"{estado['estado']} / {municipio['municipio']} / {parroquia}")
        return parroquias

    estado_id = fields.Selection(selection='_get_estados_selection', string='Estado')
    municipio = fields.Selection(selection='_get_municipios_selection', string='Municipio')
    parroquia = fields.Selection(selection='_get_parroquias_selection', string='Parroquia')

    # Relaciones
    institucion_id = fields.Many2one('sgu.institucion', 'Institución', required=True)
    carrera_ids = fields.One2many('sgu.carrera.sede', 'sede_id', string='Carreras')
```

#### 3. Nivel Académico (`sgu.nivel.academico`)

```python
class NivelAcademico(models.Model):
    _name = 'sgu.nivel.academico'
    _description = 'Nivel académico de la carrera (licenciatura, maestría, doctorado)'
    _rec_name = 'nivel'

    nivel = fields.Char('Nivel', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    carrera_ids = fields.One2many('sgu.carrera', 'nivel_academico_id', 'Carreras')
```

#### 4. Modalidad (`sgu.modalidad`)

```python
class Modalidad(models.Model):
    _name = 'sgu.modalidad'
    _description = 'Modalidad de estudio (semestral, trimestral, anual)'
    _rec_name = 'modalidad'

    modalidad = fields.Char('Modalidad', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    carrera_ids = fields.One2many('sgu.carrera', 'modalidad_id', 'Carreras')
```

#### 5. Áreas (`sgu.area`)

```python
class Area(models.Model):
    _name = 'sgu.area'
    _description = 'Áreas de la institución'
    _rec_name = 'name'

    name = fields.Char('Nombre del área', required=True)
    codigo = fields.Char('Código', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)
    telefono = fields.Char('Teléfono')
    

    # Relaciones
    carrera_ids = fields.One2many('sgu.carrera', 'area_id', 'Carreras')
```

#### 6. Carreras/Programas (`sgu.carrera`)

```python
class Carrera(models.Model):
    _name = 'sgu.carrera'
    _description = 'Programas académicos'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    codigo = fields.Char('Código', required=True)
    descripcion = fields.Text('Descripción')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    modalidad_carrera = fields.Many2one('sgu.modalidad', 'Modalidad')
    nivel_academico = fields.Many2one('sgu.nivel.academico', 'Nivel Académico')
    area_carrera = fields.Many2one('sgu.area', 'Área')
    sede_ids = fields.One2many('sgu.carrera.sede', 'carrera_id', string='Sedes disponibles')
    pensum_ids = fields.One2many('sgu.pensum', 'carrera_id', 'Pensums')
```

#### 6. Periodo Académico (`sgu.periodo`)

```python
class Periodo(models.Model):
    _name = 'sgu.periodo'
    _description = 'Periodo académico'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)  # Ej: 2025-1
    anio = fields.Integer('Año', required=True)
    periodo = fields.Selection([
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV')
    ], string='Periodo', required=True)
    modalidad = fields.Selection([
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual')
    ], string='Modalidad', required=True)
    fecha_inicio = fields.Date('Fecha inicio', required=True)
    fecha_fin = fields.Date('Fecha fin', required=True)
    active = fields.Boolean('Activo', default=True)
    descripcion = fields.Text('Descripción')

    # Relaciones
    proceso_ids = fields.One2many('sgu.proceso', 'periodo_id', 'Procesos')
```

#### 7. Proceso Académico (`sgu.proceso`)

```python
class Proceso(models.Model):
    _name = 'sgu.proceso'
    _description = 'Proceso académico'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    tipo = fields.Selection([
        ('preinscripcion', 'Preinscripción'),
        ('inscripcion', 'Inscripción'),
        ('carga_horario', 'Carga de Horarios'),
        ('carga_notas', 'Carga de Notas'),
        ('retiro', 'Retiro de materias')
    ], string='Tipo', required=True)
    periodo_id = fields.Many2one('sgu.periodo', 'Periodo', required=True)
    fecha_inicio = fields.Date('Fecha inicio', required=True)
    fecha_fin = fields.Date('Fecha fin', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('closed', 'Cerrado')
    ], string='Estado', default='draft')
    descripcion = fields.Text('Descripción')

    # Campos específicos por tipo
    carrera_ids = fields.Many2many('sgu.carrera', string='Carreras aplicables')
```

#### 8. Pensum (`sgu.pensum`)

```python
class Pensum(models.Model):
    _name = 'sgu.pensum'
    _description = 'Pensum universitario'
    _rec_name = 'name'

    name = fields.Char('Nombre', required=True)
    carrera_id = fields.Many2one('sgu.carrera', 'Carrera', required=True)
    fecha_aprobacion = fields.Date('Fecha de aprobación')
    vigente = fields.Boolean('Vigente', default=True)

    # Relaciones
    subject_ids = fields.One2many('sgu.pensum.subject', 'pensum_id', 'Materias')
```

#### 9. Materias del Pensum (`sgu.pensum.subject`)

```python
class PensumSubject(models.Model):
    _name = 'sgu.pensum.subject'
    _description = 'Materia del pensum'
    _rec_name = 'name'

    pensum_id = fields.Many2one('sgu.pensum', 'Pensum', required=True)
    code = fields.Char('Código', required=True)
    name = fields.Char('Nombre', required=True)
    semester = fields.Integer('Semestre')
    uc = fields.Integer('Unidades de Crédito')
    prelaciones = fields.Char('Prelaciones')
```

#### 10. Autoridad (`sgu.autoridad`)

```python
class Autoridad(models.Model):
    _name = 'sgu.autoridad'
    _description = 'Autoridad universitaria'
    _rec_name = 'name'

    name = fields.Char('Nombre completo', required=True)
    cargo = fields.Char('Cargo', required=True)
    firma = fields.Binary('Firma digital')
    email = fields.Char('Correo electrónico')
    active = fields.Boolean('Activo', default=True)

    # Relaciones
    sede_id = fields.Many2one('sgu.sede', 'Sede asignada')
```

#### 11. Carrera-Sede (`sgu.carrera.sede`)

```python
class CarreraSede(models.Model):
    _name = 'sgu.carrera.sede'
    _description = 'asignación  carreras a sedes'
    _rec_name = 'carrera_id'

    carrera_id = fields.Many2one('sgu.carrera', 'Carrera', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True)
    activo = fields.Boolean('Activo', default=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], string='Estado', default='draft')
    
    # Restricción de unicidad
    _sql_constraints = [
        ('carrera_sede_unique', 'unique(carrera_id, sede_id)', 
         'Ya existe esta carrera en esta sede')
    ]
```

#### 12. Horario (`sgu.horario`)

```python
class Horario(models.Model):
    _name = 'sgu.horario'
    _description = 'Horario académico'
    _rec_name = 'seccion_id'

    seccion_id = fields.Many2one('sgu.seccion', 'Sección', required=True)
    asignatura = fields.Char('Asignatura', required=True)
    profesor = fields.Char('Profesor', required=True)
    aula = fields.Char('Aula')

    dia_semana = fields.Selection([
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('7', 'Domingo')
    ], string='Día', required=True)

    hora_inicio = fields.Float('Hora inicio', required=True)
    hora_fin = fields.Float('Hora fin', required=True)
    duracion = fields.Float('Duración', compute='_compute_duracion', store=True)

    active = fields.Boolean('Activo', default=True)
```
#### 13. usuarios (`sgu.usuarios`)

```python
class Usuarios(models.Model):
    _name = 'sgu.usuarios'
   _description = 'Registro de Usuarios'
    _rec_name = 'cedula'

    primer_nombre   = fields.Char(string="Primer Nombre", required=True)
    segundo_nombre  = fields.Char(string="Segundo Nombre", required=True)
    primer_apellido = fields.Char(string="Primer Apellido", required=True)
    segundo_apellido = fields.Char(string="Segundo Apellido", required=True)
    cedula          = fields.Char(string="Cédula de identidad", required=True)
    sexo             = fields.Selection([("M","Masculino"),("F","Femenino")], string="Sexo", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento", required=True)
    etnia             = fields.Selection([("ninguno","Ninguno"),
                                          ("criollo","Criollo"),
                                          ("afrodescendiente","Afrodescendiente"),
                                          ("indigena","Indigena"),
                                          ('wayuu','Wayuu'),
                                          ('guajiro','Guajiro')],
                                         string="Etnia", required=True)
    telefono         = fields.Char(string="Teléfono", required=True)
    # Campo para definir el rol del usuario según el documento aprobado
    rol = fields.Selection([
        ('super_usuario', 'Super Usuario'),  # Gestión total del módulo, creación de usuarios, asignación de privilegios, procesos
        ('usuario_admin', 'Usuario Admin'),  # Asignación de privilegios a usuarios sectoriales
        ('operador_admin', 'Operador Admin'),  # Consultar admitidos OPSU, realizar inscripciones, generar reportes
        ('estudiante', 'Estudiante'),  # Actualizar datos, consultar horario, descargar constancias
    ], string="Rol del Usuario", required=True)
    active = fields.Boolean(string="Activo", default=True)
```



### Modelos principales - Admisión

#### 14. Aspirante (`sgu.aspirante`)

```python
class Aspirante(models.Model):
    _name = 'sgu.aspirante'
    _description = 'Aspirante a ingreso'
    _rec_name = 'cedula'

    cedula = fields.Char('Cédula', required=True, tracking=True)
    codigo_opsu = fields.Char('Código OPSU', tracking=True)

    # Datos personales
    primer_nombre = fields.Char('Primer nombre', required=True)
    segundo_nombre = fields.Char('Segundo nombre')
    primer_apellido = fields.Char('Primer apellido', required=True)
    segundo_apellido = fields.Char('Segundo apellido')
    genero = fields.Selection([('hombre','Hombre'),
                               ('mujer','Mujer')],
                              string="Género", required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    email = fields.Char(readonly=False)
    phone = fields.Char(readonly=False)
    mobile = fields.Char( readonly=False)

    # Datos adicionales
    discapacidad = fields.Boolean('Posee discapacidad')
    tipo_discapacidad = fields.Char('Tipo de discapacidad')
    etnia = fields.Selection([('ninguno','ninguno'),
                              ('guajiro','Guajiro'),],
                             string="Etnia", required=True)
    telefono = fields.Char(string="Teléfono", required=True)
    active = fields.Boolean(string="Activo", default=True)

    # Datos académicos
    tipo_asignacion = fields.Selection([
        ('opsu', 'OPSU'),
        ('rector', 'Rector'),
        ('secretaria', 'Secretaría'),
        ('dace', 'DACE'),
        ('aspirante', 'Aspirante a Cupo')
    ], string='Tipo de Asignación', required=True, default='aspirante',readonly=True)

    # Referencias a modelos base de SGU
    carrera_id = fields.Many2one('sgu.carrera', 'Programa/Carrera', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True)

    # Estado del aspirante
    state = fields.Selection([
        ('registrado', 'Registrado'),
        ('preinscrito', 'Preinscrito'),
        ('inscrito', 'Inscrito'),
        ('estudiante', 'Estudiante')
    ], string='Estado', default='registrado', tracking=True)

    # Relaciones
    preinscripcion_ids = fields.One2many('sgu_admision.preinscripcion', 'aspirante_id', 'Preinscripciones')
    inscripcion_ids = fields.One2many('sgu_admision.inscripcion', 'aspirante_id', 'Inscripciones')

    # Datos complementarios
    direccion_completa = fields.Text('Dirección completa')
    contacto_emergencia = fields.Char('Contacto de emergencia')
```

#### 15. Preinscripción (`sgu.preinscripcion`)

```python
class Preinscripcion(models.Model):
    _name = 'sgu.preinscripcion'
    _description = 'Preinscripción'
    _rec_name = 'numero_preinscripcion'

    numero_preinscripcion = fields.Char('Número', readonly=True, copy=False)
    aspirante_id = fields.Many2one('sgu.aspirante', 'Aspirante', required=True, tracking=True)
    proceso_id = fields.Many2one('sgu.proceso', 'Proceso', required=True,
                                domain="[('tipo', '=', 'preinscripcion'), ('state', '=', 'active')]")
    fecha_preinscripcion = fields.Date('Fecha', default=fields.Date.today)

    # Referencias a modelos base de SGU
    carrera_id = fields.Many2one(related='aspirante_id.carrera_id', readonly=True)
    sede_id = fields.Many2one(related='aspirante_id.sede_id', readonly=True)

    # Estado de la preinscripción
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada')
    ], string='Estado', default='draft', tracking=True)


```

#### 16. Sección (`sgu.seccion`)

```python
class Seccion(models.Model):
    _name = 'sgu.seccion'
    _description = 'Sección académica'
    _rec_name = 'codigo'

    codigo = fields.Char('Código de sección', required=True)

    # Referencias a modelos base
    carrera_id = fields.Many2one('sgu.carrera', 'Programa/Carrera', required=True)
    sede_id = fields.Many2one('sgu.sede', 'Sede', required=True)
    periodo_id = fields.Many2one('sgu.periodo', 'Periodo', required=True)

    # Capacidad
    capacidad = fields.Integer('Capacidad máxima', default=40)
    capacidad_restante = fields.Integer('Cupos disponibles', compute='_compute_capacidad_restante', store=True)

    # Relaciones
    inscripcion_ids = fields.One2many('sgu.inscripcion', 'seccion_id', 'Inscripciones')
    horario_ids = fields.One2many('sgu.horario', 'seccion_id', 'Horarios')

    active = fields.Boolean('Activo', default=True)
```

#### 17. Inscripción (`sgu.inscripcion`)

```python
class Inscripcion(models.Model):
    _name = 'sgu.inscripcion'
    _description = 'Inscripción formal'
    _rec_name = 'numero_inscripcion'

    numero_inscripcion = fields.Char('Número', readonly=True, copy=False)
    aspirante_id = fields.Many2one('sgu.aspirante', 'Aspirante', required=True, tracking=True)
    proceso_id = fields.Many2one('sgu.proceso', 'Proceso', required=True,
                               domain="[('tipo', '=', 'inscripcion'), ('state', '=', 'active')]")
    fecha_inscripcion = fields.Date('Fecha', default=fields.Date.today)

    # Referencias a modelos base
    carrera_id = fields.Many2one(related='aspirante_id.carrera_id', readonly=True)
    sede_id = fields.Many2one(related='aspirante_id.sede_id', readonly=True)

    # Sección asignada
    seccion_id = fields.Many2one('sgu.seccion', 'Sección', required=True)

    # Estado de la inscripción
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada')
    ], string='Estado', default='draft', tracking=True)

    # Documentación
    doc_cedula = fields.Boolean('Cédula entregada')
    doc_titulo = fields.Boolean('Título entregado')
    doc_notas = fields.Boolean('Notas entregadas')
    doc_fotos = fields.Boolean('Fotos entregadas')
    doc_partida = fields.Boolean('Partida de nacimiento')
    documentacion_completa = fields.Boolean('Documentos completos', compute='_compute_documentacion')

    # Relación con preinscripción
    preinscripcion_id = fields.Many2one('sgu.preinscripcion', 'Preinscripción')

    # Usuario que registró la inscripción
    usuario_inscripcion_id = fields.Many2one('res.users', 'Registrado por', default=lambda self: self.env.user)


## 🧭 Implementación del Proceso de Admisión Aprobado

### 1. Recibir Listado OPSU

- Se implementa mediante el wizard `sgu.importar.opsu.wizard` que permite:
  - Importar desde archivos CSV proporcionados por la OPSU
  - Validar campos requeridos (cédula, nombre completo, etc.)
  - Crear automáticamente registros en `sgu.aspirante` con tipo 'opsu'

### 2. Recibir Listado de Casos Aprobados

- Se implementa mediante el wizard `sgu.importar.aprobados.wizard` que permite:
  - Importar casos aprobados por autoridad universitaria
  - Seleccionar el tipo de aprobación (rector, secretaría, DACE)
  - Crear registros en `sgu.aspirante` con el tipo correspondiente

### 3. Realizar Cronograma de Inscripción

- Se implementa mediante el modelo `sgu.proceso`:
  - El Super Usuario crea y configura los procesos por carrera y sede
  - Define fechas de inicio/cierre, estatus y cupos disponibles
  - El sistema permite generar  Listar inscripción por programa y sede con cronograma segmentado

### 4. Realizar Inscripción

- El proceso implica los siguientes pasos secuenciales:

#### 🔍 Verificación de Expedientes

**Campos obligatorios** (implementados en `sgu.aspirante` y validados en el proceso):

* Cédula, nombre completo, programa, sede.
* Generación de N° de expediente (Ej: `2026-1(periodo academico del proceso en el que se realizo la inscripcion) SJM(codigo de sede)-MED( codigo de programa)-001(n° de expediente)`).
* Verificación de:
  * Mayúsculas/minúsculas.
  * Acentos.
  * Datos originales vs documentos.

**Documentos requeridos** (implementados como campos boolean en la clase `sgu.inscripcion`):

* `cedula_entregada`: Cédula de identidad (copia)
* `foto_entregada`: Foto tipo carnet
* `titulo_entregado`: Título de bachiller
* `notas_entregadas`: Notas certificadas
* `registro_opsu_entregado`: Registro OPSU
* `partida_nacimiento_entregada`: Partida de nacimiento

> ✅ Solo el **super usuario** puede modificar expedientes validados.

#### ✅ Realización de Inscripción

1. **Consulta por Cédula:** Se implementa en la barra de busqueda `buscar_por_cedula` en `sgu.aspirante`
2. **Actualización de datos personales:** Se validan en el formulario de inscripción
3. **Selección de sección y sede:** Campos en el formulario de inscripción
4. **Inscripción:** Boton `confirmar_inscripcion` que registra al estudiante
5. **Impresión de constancia:** Reporte generado desde el registro de inscripción

### 5. Módulo Estudiante

* Una vez inscrito, el aspirante pasa a ser **estudiante regular**.
* Se implementan las siguientes funcionalidades:
  * Registro de usuario en el modelo `sgu.usuarios` con rol 'estudiante'
  * Actualización de datos personales
  * Consulta de horario de clases
  * Emisión de constancias digitales


## Funcionalidades Adicionales

### 1. Wizards para Importación de Datos

El sistema incluye los siguientes asistentes para la importación masiva de datos:

#### Importación de Listados OPSU (`sgu.importar.opsu.wizard`)

Este wizard permite importar aspirantes desde archivos CSV proporcionados por la OPSU:

- **Funcionalidades**:

  - Carga de archivo CSV con listado oficial de asignados
  - Validación de campos requeridos (nombres,cédula, apellidos,codigo_opsu, programa, sede,tipo_asignacion)
  - Creación automática de registros de aspirantes
  - Detección y actualización de registros existentes
  - Asignación de tipo "opsu" a los aspirantes importados
  - Informe detallado del resultado (creados, actualizados, errores)

- **Campos principales**:
  - `archivo`: Archivo CSV a importar
  - `archivo_nombre`: Nombre del archivo
  - `delimitador`: Carácter delimitador del CSV (configuración)

#### Importación de Casos Especiales (`sgu.importar.aprobados.wizard`)

Este wizard facilita la importación de aspirantes aprobados por vías especiales:

- **Funcionalidades**:

  - Carga de archivo CSV con listado de aprobados especiales
  - Validación de campos requeridos (nombres,cédula, apellidos,codigo_opsu, programa, sede,tipo_asignacion)
  - Selección del tipo de aprobación (rector, secretaria, DACE)
  - Validación de datos y creación/actualización de aspirantes
  - Asignación automática de tipo según selección

- **Campos principales**:
  - `archivo`: Archivo CSV a importar
  - `archivo_nombre`: Nombre del archivo
  - `delimitador`: Carácter delimitador del CSV
  - `tipo_aprobacion`: Selección del tipo de caso especial

### 2. Sistema de Reportes

El módulo incluye un completo sistema de reportes que utiizara la libreria PyPDF2 :

#### Constancia de Inscripción

- **Características**:
  - Documento formal con datos completos del estudiante
  - Información de la sección asignada
  - Detalle del horario de clases
  - Registro de documentación recibida
  - Espacio para firmas y sellos oficiales
  - Verificación del funcionario que realizó la inscripción

#### Constancia de Estudio

- **Características**:
  - Formato oficial para certificar estatus de estudiante
  - Datos personales y académicos del estudiante
  - Validez institucional con firma y sellos



---
