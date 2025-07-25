from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
                            TokenObtainPairView,
                            TokenRefreshView,
                            TokenBlacklistView)
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from users.authentication import CookieJWTAuthentication


from users.serializer import (GameUserInfoSerializer, RegisterGameUserSerializer,
                            GameLogingSerializer, EmptySerializer)
from users.models import GameUsers
# Create your views here.
class RegisterGameUser(APIView):
    '''
    Create a user object
    '''
    serializer_class = RegisterGameUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameUserInfo(APIView):
    '''View to a single user
    * Only Authenticated users are able to access this view
    '''
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = GameUserInfoSerializer

    def get(self, request, *args, **kwargs):
        '''
        Return a single user based on the ID
        '''
        print(f'extra kwargs={kwargs}')
        user = get_object_or_404(GameUsers, pk=kwargs.get('pk'))
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        '''
        Update user info based on ID
        '''
        user = get_object_or_404(GameUsers, pk=kwargs.get('pk'))
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        '''
        Delete a user based on ID
        '''
        user = get_object_or_404(GameUsers, pk=kwargs.get('pk'))
        user.delete()
        return Response({"msg": "User is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

class LogInView(APIView):
    '''
    Allow users to login to the application
    '''
    serializer_class = GameLogingSerializer
    def get_tokens_for_user(self, user):
        '''
        Create a access token and refreshed token
        return a dict
        '''
        refresh = RefreshToken.for_user(user)

        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }
    
    def set_jwt_cookies_in_res(self, res_obj, token):

        res_obj.set_cookie(key='access_token',
                                value=token.get('access_token'),
                                max_age=None,
                                expires=None,
                                secure=True,
                                httponly=True,
                                samesite=None,
                                )
        res_obj.set_cookie(key='refresh_token',
                            value=token.get('refresh_token'),
                            max_age=None,
                            expires=None,
                            secure=True,
                            httponly=True,
                            samesite=None,
                            )
        return res_obj

    def post(self, request):
        print("STEP1", request.data)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_obj = serializer.validated_data
            # refresh_token = RefreshToken(user_data)
            # access_token = str(refresh_token.access_token)
            token = self.get_tokens_for_user(user_obj)
            print(f'login={token}')
            res_data = Response({'user': GameUserInfoSerializer(user_obj).data},
                                status=status.HTTP_200_OK)
            return self.set_jwt_cookies_in_res(res_data, token)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    '''
    User can logged out
    '''
    serializer_class = EmptySerializer
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        print("STEP 2", refresh_token)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (InvalidToken,ExpiredTokenError)  as e:
                print("The refresh token is invalid or expired", e)
        res = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')
        return res
    
class GetRefreshTokenView(TokenRefreshView):
    '''
    Get a new access token using the refresh token
    '''
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            response = Response({"message":"Access token is refreshed"}, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token',
                                value=access_token,
                                max_age=None,
                                expires=None,
                                secure=True,
                                httponly=True,
                                samesite='Lax')
            return response
        except InvalidToken as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ExpiredTokenError:
            return Response({"error": "Refresh token has expired"}, status=status.HTTP_403_FORBIDDEN)
