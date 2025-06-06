from django.db import models


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    game_word = models.CharField(max_length=20, null=True)
    alwd_incorrect_guess = models.PositiveIntegerField(null=True, default=0)
    incorrect_guess_made = models.PositiveIntegerField(null=True, default=0)
    incorrect_guess_remn = models.PositiveIntegerField(null=True, default=0)
    GAME_STATUS = [
        ('InProgress', 'InProgress'),
        ('Lost', 'Lost'),
        ('Won', 'Won'),
    ]
    game_status = models.CharField(max_length=30, choices=GAME_STATUS, default='InProgress')
    cur_state_word = models.CharField(max_length=30)
    guess_letter = models.CharField(max_length=5, null=True)
    guess = models.CharField(max_length=30, choices=[('Correct', 'Correct'), ('Incorrect', 'Incorrect')], default=' ')
    created_at = models.DateTimeField(auto_now_add=True)
    # is_game_over = models.BooleanField(default=False)
    # game = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.game_word
