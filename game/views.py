import random
import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from game.models import Game
from game.serializers import (GameSerializer, GameDetailSerializer, 
                              GameHelperSerializer)
from core.localcache import GameCache
from core.gamehelper import GameHelper

logger = logging.getLogger("game")

def index(request):
    '''Testing purpose'''
    return HttpResponse("Let's play the Hangman game")

class GameBaseAPI(APIView):
    '''contains all the common behaviours'''
    @staticmethod
    def makeGameResponse(game_help_obj):
        '''
        Make a proper response for the endusers
        '''

        if isinstance(game_help_obj, GameHelper):
            return GameHelperSerializer(game_help_obj).data



class CreateNewGame(APIView):
    '''Creates a new Game object'''

    def get(self, request):
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

class GameStatus(GameBaseAPI):
    '''Provide the status of the game'''
    def get(self, request, pk=None):
        """read a single game object or status"""

        game_help_obj = GameCache.get_from_cache(pk)

        if not game_help_obj:
            game_obj = get_object_or_404(Game, pk=pk)
            logger.debug('db called')
            serializer = GameSerializer(game_obj)
            data = serializer.data
            game_help_obj = GameHelper(current_state_word=data['cur_state_word'],
                                       incorrect_guess_made=data['incorrect_guess_made'],
                                       incorrect_guess_remn=data['incorrect_guess_remn'],
                                       alwd_incorrect_guess=data['alwd_incorrect_guess'],
                                       answer=data['game_word'],
                                       current_state_game=data['game_status']
                                       )
            GameCache.set_to_cache(pk, game_help_obj)
        res = self.makeGameResponse(game_help_obj)

        return Response(res, status=status.HTTP_200_OK)

class PlayGame(GameBaseAPI):
    '''Guess and Play the game'''
    def post(self, request, pk=None):
        '''Guess the letter and update the table'''
        try:
            serializer = GameDetailSerializer(data=request.data)

            if serializer.is_valid():
                guess_letter = serializer.validated_data["guess_letter"].lower()

            cached_status = GameCache.get_from_cache(pk)

            if cached_status:
                data = {
                    'answer': cached_status.answer,  # "bottle"
                    'current_state_word': cached_status.current_state_word, # str
                    'incorrect_guess_made': cached_status.incorrect_guess_made,
                    'alwd_incorrect_guess': cached_status.alwd_incorrect_guess,
                    'incorrect_guess_remn': cached_status.incorrect_guess_remn,
                    'current_state_game': cached_status.current_state_game,
                }
            else:
                game_obj = get_object_or_404(Game, pk=pk)
                data = {
                    'answer': game_obj.game_word,  # "bottle"
                    'current_state_word': game_obj.cur_state_word,  # str
                    'incorrect_guess_made': game_obj.incorrect_guess_made,
                    'alwd_incorrect_guess': game_obj.alwd_incorrect_guess,
                    'incorrect_guess_remn': game_obj.incorrect_guess_remn,
                    'current_state_game': game_obj.game_status
                }

            # returns an updated gamehelper object
            updated_status_obj = GameHelper(**data).post(guess_letter)

            GameCache.set_to_cache(pk, updated_status_obj)

            if updated_status_obj.game_over:
                self.save_final_game(pk, updated_status_obj)
            res = self.makeGameResponse(updated_status_obj)

            return Response({'status': res, "guess": updated_status_obj.guess}, status=status.HTTP_200_OK)
        except ConnectionError as e:
            logger.error("ERROR from Play Game= %s", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def save_final_game(self, pk, cached_status):
        '''save the final result to db'''
        Game.objects.filter(id=pk).update(
            incorrect_guess_made= cached_status.incorrect_guess_made,
            incorrect_guess_remn = cached_status.incorrect_guess_remn,
            game_status = cached_status.current_state_game,
            cur_state_word = cached_status.current_state_word,
        )
