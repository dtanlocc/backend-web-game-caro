from djoser.serializers  import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','email','name','password')

from .models import Room, Move,UserAccount,Board

class RoomSerializer(serializers.ModelSerializer):
    # user1 = UserCreateSerializer()
    # user2 = UserCreateSerializer()
    # winner = UserCreateSerializer()
    class Meta:
        model = Room
        fields = '__all__'

class MoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Move
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'