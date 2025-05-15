# sgu/models/pensum_model.py

from odoo import fields, models, api
import json # Necesitas importar json
from odoo.exceptions import ValidationError


class SguPensum(models.Model):
    _name = 'sgu.pensum'
    _description = 'Pensum Universitario Dinámico (Alternativo)'

    name = fields.Char(string="Nombre del Pensum", compute="_compute_name", store=True)
    codigo_principal = fields.Integer(string="Código Principal")
    is_trimestre_mode = fields.Boolean(string="Modo Trimestre", default=False)

    
    # Cambiar campos Selection por relaciones Many2one
    modalidad = fields.Many2one(
        'sgu_modalidad', 
        string="Modalidad", 
        required=True
    )
    
    nivel_academico = fields.Many2one(
        'sgu_nivel_academico', 
        string="Nivel Académico", 
        required=True
    )
    
    carrera = fields.Many2one(
        'sgu_carreras', 
        string="Carrera", 
        required=True
    )
    
    period_count = fields.Integer(string="Número de Divisiones/Trayectos", default=1)
    assignment_data = fields.Text(string="Datos de Asignaturas (JSON)")
        # Campo computado para mostrar en la vista
    assignment_table = fields.Html(
        string="Tabla de Asignaturas",
        compute="_compute_assignment_table",
        sanitize=False
    )
    @api.constrains('assignment_data')
    def _check_assignment_data(self):
        for rec in self:
            if rec.assignment_data:
                try:
                    data = json.loads(rec.assignment_data)
                    if not isinstance(data, list):
                        raise ValidationError("Formato inválido para assignment_data.")
                except json.JSONDecodeError:
                    raise ValidationError("JSON inválido en assignment_data.")    

    @api.depends('carrera', 'nivel_academico', 'modalidad')
    def _compute_name(self):
        for pensum in self:
            name_parts = [
                pensum.carrera.carrera if pensum.carrera else '',
                pensum.nivel_academico.nivel if pensum.nivel_academico else '',
                pensum.modalidad.modalidad if pensum.modalidad else ''
            ]
            pensum.name = "Pensum " + " - ".join(p for p in name_parts if p)

    @api.depends('assignment_data')
    def _compute_assignment_table(self):
        for rec in self:
            if not rec.assignment_data:
                rec.assignment_table = "<p>No hay asignaturas guardadas.</p>"
                continue

            try:
                rows = json.loads(rec.assignment_data)
                html = self._generate_html_table(rows, rec.modalidad.modalidad, rec.is_trimestre_mode)
                rec.assignment_table = html
            except Exception as e:
                rec.assignment_table = f"<p>Error al cargar datos: {str(e)}</p>"


    # En _generate_html_table (Python)
    def _generate_html_table(self, rows, modalidad, modo_trayecto):
        tables = []
        divisions = sorted({row['division'] for row in rows})

        for div in divisions:
            div_rows = [r for r in rows if r['division'] == div]
            if modo_trayecto:
                etiqueta_encabezado = "Trayecto"
            else:
                etiqueta_encabezado = modalidad
            table = f"""
                <div class="pensum-table-section">
                    <h4>{etiqueta_encabezado} {div}</h4>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Código</th>
                                <th>Asignatura</th>
                                <th>UC</th>
                                <th>H. Teóricas</th>
                                <th>H. Prácticas</th>
                                <th>H. Totales</th>
                                <th>Prelación</th>
                            </tr>
                        </thead>
                        <tbody>
            """

            for row in div_rows:
                # Construir el texto de prelación
                prel_asigs = row.get('prelAsigs', []) or []
                prel_uc = row.get('prelUC', 0) or 0
                prel_gaceta = row.get('prelGaceta', '') or ''

                prel_text = (
                    f"Asignaturas: {', '.join(prel_asigs) if prel_asigs else '-'}; "
                    f"UC: {prel_uc}; "
                    f"Gaceta: {prel_gaceta if prel_gaceta else '-'}"
                )

                # Generar fila
                table += f"""
                            <tr>
                                <td>{row.get('codigo', '')}</td>
                                <td>{row.get('asignatura', '')}</td>
                                <td>{row.get('uc', 0)}</td>
                                <td>{row.get('ht', 0)}</td>
                                <td>{row.get('hp', 0)}</td>
                                <td>{row.get('tot', 0)}</td>
                                <td>{prel_text}</td>
                            </tr>
                """

            table += """
                        </tbody>
                    </table>
                </div>
            """
            tables.append(table)

        return "".join(tables)
# Ya NO existe el modelo SguPensumAssignment en esta alternativa
# class SguPensumAssignment(...):
#    ...