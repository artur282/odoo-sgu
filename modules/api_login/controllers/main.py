from odoo import http
from odoo.http import request
import requests

class APILoginController(http.Controller):

    @http.route('/login_api', type='http', auth='public', website=True, csrf=False)
    def login_api_form(self, **kw):
        # Verificar si el usuario ya ha iniciado sesión mediante la API
        access_token = request.session.get('access_token')
        if access_token:
            # Si ya ha iniciado sesión, redirigir a la página protegida
            return request.redirect('/protected_page')

        # Mostrar el formulario de inicio de sesión
        return request.render('api_login.login_api_template', {})

    @http.route('/login_api/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def login_api_submit(self, **post):
        email = post.get('email')
        password = post.get('password')

        try:
            # Enviar solicitud a la API externa
            response = requests.post(
                'https://sgu.casacam.net/api/v1/login',
                data={
                    'grant_type': '',
                    'username': email,
                    'password': password,
                    'scope': '',
                    'client_id': '',
                    'client_secret': ''
                },
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            response.raise_for_status()
            data = response.json()

            if data.get('access_token'):
                # Almacenar el token en la sesión del usuario
                request.session['access_token'] = data['access_token']

                # Redirigir a la página protegida
                return request.redirect('/protected_page')
            else:
                # Si las credenciales son inválidas, mostrar mensaje de error
                return request.render('api_login.login_api_template', {'error': 'Credenciales inválidas. Por favor, intenta de nuevo.'})

        except requests.exceptions.HTTPError as e:
            return request.render('api_login.login_api_template', {
                'error': f'Error de autenticación: {str(e)}',
            })

        except requests.exceptions.RequestException as e:
            # Error al conectar con la API externa
            return request.render('api_login.login_api_template', {'error': f'Error al conectar con la API externa: {e}'})
        except Exception as e:
            # Otro tipo de error
            return request.render('api_login.login_api_template', {'error': f'Ocurrió un error: {e}'})

    @http.route('/protected_page', type='http', auth='public', website=True)
    def protected_page(self, **kw):
        # Verificar si el usuario tiene el token de acceso
       
        return request.render('api_login.protected_page_template_2')

    @http.route('/logout_api', type='http', auth='public', website=True)
    def logout_api(self, **kw):
        # Eliminar el token de la sesión
        request.session.pop('access_token', None)
        # Redirigir al formulario de inicio de sesión
        return request.redirect('/login_api')