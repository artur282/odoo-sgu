from odoo import http
from odoo.http import request

class PeriodoAcademicoController(http.Controller):

    @http.route(['/periodo_academico'], type='http', auth='public', csrf=False, website=True)
    def periodo_academico(self, **kwargs):
        periodos = request.env['periodo.academico'].sudo().search([])
        return request.render('periodo_academico.template_periodo_academico', {'periodos': periodos})

    @http.route('/newPeriodo', type='http', auth='public', methods=['POST'], csrf=False)
    def new_periodo(self, **post):
        request.env['periodo.academico'].sudo().create({
            'ano': int(post.get('año')) if post.get('año') else 0,
            'tipo': post.get('tipo'),
            'periodo': post.get('periodo'),
            'status': post.get('Status'),
        })
        return request.redirect('/periodo_academico')

    @http.route('/cambiar_status/<int:record_id>', type='http', auth='public', csrf=False)
    def cambiar_status(self, record_id, **kwargs):
        record = request.env['periodo.academico'].sudo().browse(record_id)
        if record:
            record.cambiar_status()
        return request.redirect('/periodo_academico')
