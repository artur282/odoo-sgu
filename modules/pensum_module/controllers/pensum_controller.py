from odoo import http
from odoo.http import request

class PensumController(http.Controller):

    @http.route('/pensum', type='http', auth="public", website=True)
    def pensum_form(self, **kw):
        # Obtenemos los registros existentes para mostrarlos en el selector de prelaciones
        records = request.env['pensum.record'].sudo().search([])
        return request.render('pensum_module.pensum_form_template', {'records': records})

    @http.route('/pensum/save', type='http', auth='public', website=True, methods=['POST'])
    def pensum_save(self, **post):
        # Capturamos los datos del formulario principal
        semestre = post.get('semestre')
        codigo = post.get('codigo')
        asignatura = post.get('asignatura')
        uc = post.get('uc')
        prelacion = post.get('prelacion')

        # Creamos el registro principal
        request.env['pensum.record'].sudo().create({
            'semestre': semestre,
            'codigo': codigo,
            'asignatura': asignatura,
            'uc': uc,
            'prelacion': prelacion,
        })

        # Si se han agregado campos adicionales, puedes procesarlos de forma similar
        # Ejemplo: procesamos arrays de campos extra (esto requeriría lógica adicional)

        return request.redirect('/pensum/view')

    @http.route('/pensum/view', type='http', auth='public', website=True)
    def pensum_view(self, **kwargs):
        # Buscamos todos los registros creados
        records = request.env['pensum.record'].sudo().search([])
        return request.render('pensum_module.pensum_view_template', {
            'records': records,
        })
