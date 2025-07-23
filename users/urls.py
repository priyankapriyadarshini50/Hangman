from django.urls import path
from users.views import (RegisterGameUser, GameUserInfo,
                         LogInView, LogOutView,
                         GetRefreshTokenView)

urlpatterns = [
    path('<int:pk>/', GameUserInfo.as_view(), name='users-info'),
    path('register/', RegisterGameUser.as_view(), name='create-user'),
    path('login/', LogInView.as_view(), name='user-login'),
    path('logout/', LogOutView.as_view(), name='user-logout'),
    path('refresh-token/', GetRefreshTokenView.as_view(), name='refresh-token'),
]
