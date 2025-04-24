'''this module defines the helper class and associated methods'''
from typing import List
class GameHelper:
    '''
    This class has static methods and hold the logic of the game
    '''

    @staticmethod
    def create_cache_status(*args):
        '''
        Create a chached data structure before caching
        '''
        return {
            'current_state_game': args[0],
            'current_state_word': args[1],
            'number of incorrect guesses already made': args[2],
            'number of incorrect guesses remaining': args[3],
            'answer': args[4],
            'alwd_incorrect_guess': args[5],
        }

    @staticmethod
    def get_game_status(incorrect_guess_remn: int, cur_state_word: str):
        """return the status of game"""
        if (incorrect_guess_remn == 0) and ("_" in cur_state_word):
            return "Lost"
        elif (incorrect_guess_remn >= 0) and ("_" not in cur_state_word):
            return "Won"
        else:
            return "InProgess"

    @staticmethod
    def get_guessed_data(guess_letter: str, answer: str, current_state_word: List):
        """check if the guessing letter is correct or not
        returns a tuple with str values
        """
        guess = "Incorrect"
        new_state_word = list(current_state_word)
        if guess_letter in answer:
            guess = 'Correct'
            for indx, ch in enumerate(list(answer)):
                if ch == guess_letter:
                    new_state_word[indx] = ch.upper() if indx == 0 else ch
        return guess, ''.join(new_state_word)
