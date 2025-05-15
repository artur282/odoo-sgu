# controllers/pensum_controller.py
from odoo import http
from odoo.http import request

class PensumController(http.Controller):

    # @http.route('/uni/pensum/get_options', type='json', auth='public')
    # def get_options(self):
    #     # devolver listas de modalidades, niveles y carreras
    #     return {
    #         'modalidades': request.env['sgu_modalidad']
    #                              .search_read([], ['id', 'modalidad']),
    #         'niveles':    request.env['sgu_nivel_academico']
    #                              .search_read([], ['id', 'nivel']),
    #         'carreras':   request.env['sgu_carreras']
    #                              .search_read([], ['id', 'carrera']),
    #     }

    @http.route('/uni/pensum/lines', type='json', auth='user')
    def get_lines(self, pensum_vals):
        # pensum_vals = {modalidad_id, nivel_id, carrera_id, codigo}
        pensum = request.env['uni.pensum'].search(pensum_vals, limit=1)
        return pensum and pensum.line_ids.read() or []

    @http.route('/uni/pensum/line/create', type='json', auth='public')
    def create_line(self, vals):
        line = request.env['uni.pensum.line'].create(vals)
        return line.read()[0]

    @http.route('/uni/pensum/line/write', type='json', auth='public')
    def write_line(self, id, vals):
        rec = request.env['uni.pensum.line'].browse(id)
        rec.write(vals)
        return True

    @http.route('/uni/pensum/line/unlink', type='json', auth='public')
    def unlink_line(self, id):
        request.env['uni.pensum.line'].browse(id).unlink()
        return True
