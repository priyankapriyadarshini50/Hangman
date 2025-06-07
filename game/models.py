from django.db import models
from users.models import GameUsers


class Game(models.Model):
    '''
    Creates and saves a game instace
    '''

    GAME_STATUS = [
        ('InProgress', 'InProgress'),
        ('Lost', 'Lost'),
        ('Won', 'Won'),
    ]
    GUESS_STATUS = [
        ('Correct', 'Correct'),
        ('Incorrect', 'Incorrect')
        ]
    id = models.BigAutoField(primary_key=True)
    game_word = models.CharField(max_length=20, null=True)
    alwd_incorrect_guess = models.PositiveIntegerField(null=True, default=0)
    incorrect_guess_made = models.PositiveIntegerField(null=True, default=0)
    incorrect_guess_remn = models.PositiveIntegerField(null=True, default=0)
    game_status = models.CharField(max_length=30, choices=GAME_STATUS, default='InProgress')
    cur_state_word = models.CharField(max_length=30)
    guess_letter = models.CharField(max_length=5, null=True)
    guess = models.CharField(max_length=30, choices=GUESS_STATUS, default=' ')
    created_at = models.DateTimeField(auto_now_add=True)
    is_game_over = models.BooleanField(default=False)
    gameuser = models.ForeignKey(GameUsers, on_delete=models.CASCADE,
                                 null=True, blank=True)

    def __str__(self):
        return self.game_word
