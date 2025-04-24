import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from game.models import Game
from game.serializers import GameSerializer, GameDetailSerializer
from core.localcache import GameCache
from core.gamehelper import GameHelper



def index(request):
    '''Testing purpose'''
    return HttpResponse("Let's play the Hangman game")


class GameViewSet(viewsets.ViewSet):
    '''Viewset creates all the three API endpoints'''

    def list(self, request):
        """Create a game object with default values"""
        game_word = random.choice(["Hangman", "Python", "Django", "Bottle", "Pen"]).lower()
        alwd_incorrect_guess = round(len(game_word) / 2)
        incorrect_guess_made = 0
        incorrect_guess_remn = alwd_incorrect_guess - incorrect_guess_made
        cur_state_word = '_' * len(game_word)
        queryset = Game.objects.create(game_word=game_word,
                                       alwd_incorrect_guess=alwd_incorrect_guess,
                                       cur_state_word=cur_state_word,
                                       incorrect_guess_remn=incorrect_guess_remn,
                                       incorrect_guess_made=incorrect_guess_made)
        serializer = GameSerializer(queryset)
        data = {'id': serializer.data['id']}
        return Response(data, status=status.HTTP_200_OK) # JSONRender

    def retrieve(self, request, pk=None):
        """read a single game object or status"""

        cached_status = GameCache.get_from_cache(pk)
        if not cached_status:
            game_obj = get_object_or_404(Game, pk=pk)
            serializer = GameSerializer(game_obj)
            data = serializer.data
            cached_status = GameHelper.create_cache_status(
                data['game_status'],
                data['cur_state_word'],
                data['incorrect_guess_made'],
                data['incorrect_guess_remn'], data['game_word'],
                data['alwd_incorrect_guess'])
            GameCache.set_to_cache(pk, cached_status)
        cached_status.pop('answer')

        return Response(cached_status)

    def save_final_game(self, pk, cached_status):
        '''save the final result to db'''
        Game.objects.filter(id=pk).update(
            incorrect_guess_made= cached_status.get('number of incorrect guesses already made'),
            incorrect_guess_remn = cached_status.get('number of incorrect guesses remaining'),
            game_status = cached_status.get('current_state_game'),
            cur_state_word = cached_status.get('current_state_word'),
        )

    @action(methods=['post'], detail=True, url_path='guess', url_name='game_logic')
    def guess(self, request, pk=None):
        '''Guess the letter and update the table'''
        try:
            serializer = GameDetailSerializer(data=request.data)

            if serializer.is_valid():
                guess_letter = serializer.validated_data["guess_letter"].lower()

            cached_status = GameCache.get_from_cache(pk)

            if not cached_status:
                game_obj = get_object_or_404(Game, pk=pk)
                answer = game_obj.game_word  # "bottle"
                current_state_word = list(game_obj.cur_state_word)  # [_ _ _ _ _ _]
                incorrect_guess_made = game_obj.incorrect_guess_made
                alwd_incorrect_guess = game_obj.alwd_incorrect_guess
                incorrect_guess_remn = game_obj.incorrect_guess_remn
            else:
                answer = cached_status.get('answer')  # "bottle"
                current_state_word = list(cached_status.get('current_state_word')) # [_ _ _ _ _ _]
                incorrect_guess_made = cached_status.get('number of incorrect guesses already made')
                alwd_incorrect_guess = cached_status.get('alwd_incorrect_guess')
                incorrect_guess_remn = cached_status.get('number of incorrect guesses remaining')

            guess_value, current_state_word = GameHelper.get_guessed_data(
                guess_letter, answer, current_state_word)

            if guess_value == 'Incorrect':
                incorrect_guess_made = incorrect_guess_made + 1
                incorrect_guess_remn = alwd_incorrect_guess - incorrect_guess_made

            game_status = GameHelper.get_game_status(incorrect_guess_remn, current_state_word)

            cached_status = GameHelper.create_cache_status(
                    game_status,
                    current_state_word,
                    incorrect_guess_made,
                    incorrect_guess_remn, answer,
                    alwd_incorrect_guess)
            GameCache.set_to_cache(pk, cached_status)
            cached_status.pop('answer')
            if game_status in ['Won', "Lost"]:
                self.save_final_game(pk, cached_status)

            data = {'status': cached_status,
                    "guess": guess_value}
            return Response(data, status=status.HTTP_200_OK)
        except ConnectionError as e:
            print(f"ERROR={e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
