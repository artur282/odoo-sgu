from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests

class LoginAPI(models.TransientModel):
    _name = 'login.api.wizard'
    _description = 'Wizard para login con API externa'

    email = fields.Char(string="Correo electrónico", required=True)
    password = fields.Char(string="Contraseña", required=True)

    def login(self):
        self.ensure_one()
        try:
            # Enviar solicitud a la API externa
            response = requests.post(
                'https://sgu.casacam.net/api/v1/login',
                data={
                    'grant_type': '',
                    'username': self.email,
                    'password': self.password,
                    'scope': '',
                    'client_id': '',
                    'client_secret': ''
                },
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            response.raise_for_status()  # Lanza excepción para códigos de error HTTP
            data = response.json()

            if data.get('access_token'):
                # Almacenar el token en la sesión del usuario
                session_token = data['access_token']
                request = self.env['ir.http'].request
                if request:
                    request.session['access_token'] = session_token

                # Redirigir a la página protegida
                return {
                    'type': 'ir.actions.act_url',
                    'url': '/protected_page',
                    'target': 'self',
                }
            else:
                raise ValidationError(_('Credenciales inválidas. Por favor, intenta de nuevo.'))

        except requests.exceptions.RequestException as e:
            raise ValidationError(_('Error al conectar con la API externa: %s') % e)
        except Exception as e:
            raise ValidationError(_('Ocurrió un error: %s') % e)
