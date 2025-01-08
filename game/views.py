from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Game
from .serializers import GameSerializer, GameDetailSerializer
import random


def index(request):
    return HttpResponse("Hello World")


class GameViewSet(viewsets.ViewSet):

    def list(self, request):
        game_word = random.choice(["Hangman", "Python", "Django", "Bottle", "Pen"]).lower()
        alwd_incorrect_guess = round(len(game_word) / 2)
        incorrect_guess_made = 0
        incorrect_guess_remn = alwd_incorrect_guess - incorrect_guess_made
        cur_state_word = '_' * len(game_word)
        queryset = Game.objects.create(game_word=game_word, alwd_incorrect_guess=alwd_incorrect_guess,
                                       cur_state_word=cur_state_word, incorrect_guess_remn=incorrect_guess_remn,
                                       incorrect_guess_made=incorrect_guess_made)
        serializer = GameSerializer(queryset)
        data = {'id': serializer.data['id']}
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Game.objects.all()
        game_obj = get_object_or_404(queryset, pk=pk)
        serializer = GameSerializer(game_obj)
        data = serializer.data
        game_status = {'current_state_game': data['game_status'],
                       'current_state_word': data['cur_state_word'],
                       'number of incorrect guesses already made': data['incorrect_guess_made'],
                       'number of incorrect guesses remaining': data['incorrect_guess_remn']}
        return Response(game_status)

    @action(methods=['post'], detail=True, url_path='guess', url_name='game_logic')
    def guess(self, request, pk=None):

        queryset = Game.objects.all()
        game_obj = get_object_or_404(queryset, pk=pk)

        serializer = GameDetailSerializer(game_obj, data=request.data)
        if serializer.is_valid():
            guess_letter = serializer.validated_data['guess_letter'].lower()
            answer = game_obj.game_word  # "bottle"
            current_state_word = list(game_obj.cur_state_word)  # [_ _ _ _ _ _]

            if guess_letter in answer:
                game_obj.guess = 'Correct'
                for index, ch in enumerate(list(answer)):
                    if ch == guess_letter:
                        if index == 0:
                            current_state_word[index] = ch.upper()
                        else:
                            current_state_word[index] = ch
                        game_obj.cur_state_word = ''.join(current_state_word)
            else:
                game_obj.guess = 'Incorrect'
                game_obj.incorrect_guess_made = game_obj.incorrect_guess_made + 1
                game_obj.incorrect_guess_remn = game_obj.alwd_incorrect_guess - game_obj.incorrect_guess_made

            if (game_obj.incorrect_guess_remn == 0) and ("_" in game_obj.cur_state_word):
                game_obj.game_status = "Lost"
            elif (game_obj.incorrect_guess_remn >= 0) and ("_" not in game_obj.cur_state_word):
                game_obj.game_status = "Won"
            else:
                game_obj.game_status = "InProgess"

            game_obj.save()
            res_obj = self.retrieve(request, pk=pk)
            data1 = res_obj.data
            data = {'status': data1,"guess": game_obj.guess}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
