from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    '''
    Creating a cookie based authentication
    '''
    def authenticate(self, request):
        print("Cookie authentication")
        token = request.COOKIES.get("access_token")
        print(token)
        if not token:
            return None
        try:
            validated_token = self.get_validated_token(token)
            print(f"Validated Token={validated_token}")
            user = self.get_user(validated_token)
            return user, validated_token
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f'Token validation Failed: {e}')

