# -*- coding: utf-8 -*-
# from odoo import http


# class Sgu(http.Controller):
#     @http.route('/sgu/sgu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sgu/sgu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sgu.listing', {
#             'root': '/sgu/sgu',
#             'objects': http.request.env['sgu.sgu'].search([]),
#         })

#     @http.route('/sgu/sgu/objects/<model("sgu.sgu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sgu.object', {
#             'object': obj
#         })

