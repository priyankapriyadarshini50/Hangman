from rest_framework import serializers
from game.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class GameDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['guess_letter']

    def validate_guess_letter(self, value: str):
        '''validate the user input letter'''
        if value in {'', ' '} and value.isalpha():
            raise serializers.ValidationError(
                "Please enter a Valid Letter"
            )
        return value

class GameHelperSerializer(serializers.Serializer):
    '''serializer class make the response of the game'''
    current_state_game = serializers.CharField()
    current_state_word = serializers.CharField()
    number_of_incorrect_guesses_already_made = serializers.CharField(source='incorrect_guess_made')
    number_of_incorrect_guesses_remaining = serializers.CharField(source='incorrect_guess_remn')
