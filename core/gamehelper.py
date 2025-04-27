'''this module defines the helper class and associated methods'''
from typing import List
class GameHelper:
    '''
    This class has static methods and hold the logic of the game
    '''
    def __init__(self, game_over=False, guess=None, **kwargs):
        self.answer = kwargs.get('answer')
        self.current_state_word: str = kwargs.get('current_state_word')
        self.current_state_game = kwargs.get('current_state_game') #Win/Lost
        self.incorrect_guess_made = kwargs.get('incorrect_guess_made')
        self.alwd_incorrect_guess = kwargs.get('alwd_incorrect_guess')
        self.incorrect_guess_remn = kwargs.get('incorrect_guess_remn')
        self.game_over = game_over #true/false
        self.guess = guess #correct/Incorrect


    def post(self, guessed_letter):
        if guessed_letter:

            if self.alwd_incorrect_guess == self.incorrect_guess_made:
                self.game_over = True
                return self

            self.guess = self.get_guessed_data(guessed_letter)
            if self.guess == 'Incorrect':
                self.incorrect_guess_made += 1
                self.incorrect_guess_remn = self.alwd_incorrect_guess - self.incorrect_guess_made

            self.current_state_game = self.get_game_status()

            return self

    def get_game_status(self) -> str:
        """return the status of game"""
        if (self.incorrect_guess_remn == 0) and ("_" in self.current_state_word):
            return "Lost"
        elif (self.incorrect_guess_remn >= 0) and ("_" not in self.current_state_word):
            return "Won"
        else:
            return "InProgess"


    def get_guessed_data(self, guess_letter: str):
        """check if the guessing letter is correct or not
        returns a tuple with str values
        """
        guess = "Incorrect"
        new_state_word = list(self.current_state_word)
        if guess_letter in self.answer:
            guess = 'Correct'
            for indx, ch in enumerate(list(self.answer)):
                if ch == guess_letter:
                    new_state_word[indx] = ch.upper() if indx == 0 else ch
        self.current_state_word = ''.join(new_state_word)
        return guess
