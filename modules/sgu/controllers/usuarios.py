from odoo import http
from odoo.http import request

class UserRegistrationController(http.Controller):

    # @http.route(['/user_registration'], type='http', auth='public', website=True)
    # def registration_page(self, **kwargs):
    #     registros = request.env['user.registration'].sudo().search([])
    #     return request.render('registro_usuarios.user_registration_template', {'registros': registros})


    @http.route('/user_registration/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_user(self, **post):
        # Mapear los valores recibidos del formulario con los campos del modelo
        values = {
            'primer_nombre': post.get('primerNombre'),
            'segundo_nombre': post.get('segundoNombre'),
            'primer_apellido': post.get('primerApellido'),
            'segundo_apellido': post.get('segundoApellido'),
            'cedula': int(post.get('cedula')) if post.get('cedula') else 0,
            'correo': post.get('correo'),
            'genero': post.get('genero'),
            'fecha_nacimiento': post.get('fechaNacimiento'),
            'discapacidad': post.get('discapacidad'),
            'etnia': post.get('etnia'),
            'telefono': post.get('telefono'),
            'grupo_usuario': post.get('grupoUsuario'),
        }
        request.env['user.registration'].sudo().create(values)
        return request.redirect('/user_registration')
