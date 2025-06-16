from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    '''
    Cchecking a cookie based authentication
    This is a custom middleware to extract token from cookies
    '''
    def check_auth_header(self, request):
        '''
        Check for JWT token in the Authorization header
        '''
        return super().authenticate(request)

    def authenticate(self, request):
        print("Cookie authentication")

        # Look for JWT in the "Authorization" header
        auth_header = self.check_auth_header(request)
        if auth_header:
            return auth_header

        token = request.COOKIES.get("access_token")
        print('found the token')
        if not token:
            return None
        try:
            validated_token = self.get_validated_token(token)

            user = self.get_user(validated_token)
            return user, validated_token
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f'Token validation Failed: {e}')
