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
