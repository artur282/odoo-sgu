# -*- coding: utf-8 -*-
# from odoo import http


# class Usuarios(http.Controller):
#     @http.route('/usuarios/usuarios', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/usuarios/usuarios/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('usuarios.listing', {
#             'root': '/usuarios/usuarios',
#             'objects': http.request.env['usuarios.usuarios'].search([]),
#         })

#     @http.route('/usuarios/usuarios/objects/<model("usuarios.usuarios"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('usuarios.object', {
#             'object': obj
#         })

