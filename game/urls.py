from django.urls import path
from game.views import (CreateNewGame, GameStatus, PlayGame)

urlpatterns = [
    path('new/', CreateNewGame.as_view()),
    path('<int:pk>/', GameStatus.as_view()),
    path('<int:pk>/guess/', PlayGame.as_view()),
]
