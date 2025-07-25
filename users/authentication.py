import logging
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

django_logger = logging.getLogger('django')

class CookieJWTAuthentication(JWTAuthentication):
    '''
    Checking a cookie based authentication
    This is a custom global middleware to extract token from cookies
    before each view is called
    It will check for the JWT token in the cookies first,
    '''
    def check_auth_header(self, request):
        '''
        Check for JWT token in the Authorization header
        '''
        return super().authenticate(request)
    
    def is_public_path(self, path):
        '''Check if the path is public and does not require authentication'''
        return path in settings.API_WHITELISTED_PATHS

    def authenticate(self, request):
        print("Cookie authentication")

        # Look for JWT in the "Authorization" header
        auth_header = self.check_auth_header(request)
        if auth_header:
            return auth_header
        
        # exclude authentication for swagger and redoc
        if self.is_public_path(request.path):
            return None

        raw_token = request.COOKIES.get("access_token")
        if raw_token:
            print('found the token')
        if not raw_token:
            return None
        try:
            validated_token = self.get_validated_token(raw_token) # raise Validation error
            user = self.get_user(validated_token)
            return user, validated_token
        except AuthenticationFailed as e:
            django_logger.error(f"Token error: {e}")
            raise AuthenticationFailed({
                "detail": "Your token is expired or invalid"
            })
       
