import random
from typing import List
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Game
from .serializers import GameSerializer, GameDetailSerializer



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
        queryset = Game.objects.create(game_word=game_word, alwd_incorrect_guess=alwd_incorrect_guess,
                                       cur_state_word=cur_state_word, incorrect_guess_remn=incorrect_guess_remn,
                                       incorrect_guess_made=incorrect_guess_made)
        serializer = GameSerializer(queryset)
        data = {'id': serializer.data['id']}
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """read a single game object or status"""

        game_obj = get_object_or_404(Game, pk=pk)
        serializer = GameSerializer(game_obj)
        data = serializer.data
        game_status = self.update_response_status(data['game_status'], data['cur_state_word'],
                                                 data['incorrect_guess_made'], data['incorrect_guess_remn'])

        return Response(game_status)
    
    def get_guessed_data(self,guess_letter: str, answer: str, current_state_word: List):
        """check if the guessing letter is correct or not
        returns a tuple with str values
        """
        guess = "Incorrect"
        new_state_word = list(current_state_word)
        if guess_letter in answer:
            guess = 'Correct'
            for indx, ch in enumerate(list(answer)):
                if ch == guess_letter: 
                    if indx == 0:
                        new_state_word[indx] = ch.upper()
                    else:
                        new_state_word[indx] = ch
        return guess, ''.join(new_state_word)
    
    def get_game_status(self, incorrect_guess_remn: int, cur_state_word: str):
        """return the status of game"""
        if (incorrect_guess_remn == 0) and ("_" in cur_state_word):
            game_status = "Lost"
        elif (incorrect_guess_remn >= 0) and ("_" not in cur_state_word):
            game_status = "Won"
        else:
            game_status = "InProgess"
        return game_status
    
    def update_response_status(self, *args):
        '''structure the response data'''
        status = {}
        status['current_state_game'] = args[0]
        status['current_state_word'] = args[1]
        status['number of incorrect guesses already made'] = args[2]
        status['number of incorrect guesses remaining'] = args[3]
        return status


    @action(methods=['post'], detail=True, url_path='guess', url_name='game_logic')
    def guess(self, request, pk=None):
        '''Guess the letter and update the table'''
        game_obj = get_object_or_404(Game, pk=pk)

        serializer = GameDetailSerializer(game_obj, data=request.data)
        if serializer.is_valid():
            guess_letter = serializer.validated_data['guess_letter'].lower()
            answer = game_obj.game_word  # "bottle"
            current_state_word = list(game_obj.cur_state_word)  # [_ _ _ _ _ _]
            incorrect_guess_made = game_obj.incorrect_guess_made
            alwd_incorrect_guess = game_obj.alwd_incorrect_guess
            incorrect_guess_remn = game_obj.incorrect_guess_remn

            guess_value, current_state_word = self.get_guessed_data(
                guess_letter, answer, current_state_word)

            if guess_value == 'Incorrect':
                incorrect_guess_made = incorrect_guess_made + 1
                incorrect_guess_remn = alwd_incorrect_guess - incorrect_guess_made

            game_status = self.get_game_status(incorrect_guess_remn, current_state_word)

            game_obj.guess = guess_value
            game_obj.cur_state_word = current_state_word
            game_obj.incorrect_guess_made = incorrect_guess_made
            game_obj.incorrect_guess_remn = incorrect_guess_remn
            game_obj.game_status = game_status
            game_obj.save(update_fields=["guess", "cur_state_word", "incorrect_guess_made",
                                         "incorrect_guess_remn", "game_status"])

            gm_status = self.update_response_status(game_status, current_state_word,
                                        incorrect_guess_made, incorrect_guess_remn)
            data = {'status': gm_status,
                    "guess": game_obj.guess}
            return Response(data, status=status.HTTP_200_OK)
  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
