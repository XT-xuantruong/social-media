from rest_framework import serializers

from .models import User, FriendshipRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('id', 'name', 'email', 'friends_count', 'posts_count', 'avatar')
=======
        fields = ('id', 'name', 'email', 'friends_count','avatar', 'posts_count')
>>>>>>> 4bddc1161a5398f5e73e8e4faa0df77adf537c53

class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by',)