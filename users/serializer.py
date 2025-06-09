from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import GameUsers

class RegisterGameUserSerializer(serializers.ModelSerializer):
    '''Serilizer for new user'''
    class Meta:
        model = GameUsers
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class GameUserInfoSerializer(serializers.ModelSerializer):
    '''
    serialize/deserialize a single user data
    (convert from complex object to python data types)
    '''
    class Meta:
        model = GameUsers
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'last_login')

class GameLogingSerializer(serializers.Serializer):
    '''
    serialize/deserialize the login data
    '''
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'},
                                     min_length=8)

    def validate_email(self, value):
        '''
        Check the email contains @ special character
        '''
        if "@" not in value:
            raise serializers.ValidationError("Please provide a valid email")
        return value

    def validate(self, data):
        '''
        Validate user input data
        Django authentication validate with username and password
        '''
        print("STEP2", data)
        # authentication required with email and password
        # need to overrride the method
        user = authenticate(request=None, **data)
        print(user)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")
