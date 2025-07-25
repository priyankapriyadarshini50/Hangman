"""hangman_rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
                            TokenObtainPairView,
                            TokenRefreshView,
                            TokenBlacklistView)
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView,
                                   SpectacularRedocView)
from rest_framework.permissions import AllowAny
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/game/', include("game.urls")),
    path('api/v1/users/', include("users.urls")),
    path('', views.index, name='index'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(), name='redoc'),
]
