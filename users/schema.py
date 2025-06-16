'''
For adding a schema for custom authentication class, so that swagger doc can interprete 
custom authentication
'''

# users/schema.py or any schema.py file

from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CookieJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'users.authentication.CookieJWTAuthentication'  # full import path
    name = 'cookieJWT'  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access_token',
        }
