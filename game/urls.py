from .views import GameViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'new', GameViewSet, basename='new')
urlpatterns = [
    # path('', include(router.urls)),
    path('new/', GameViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', GameViewSet.as_view({'get': 'retrieve'})),
    path('<int:pk>/guess/', GameViewSet.as_view({'post': 'guess'})),
]
