from rest_framework import serializers

from .models import User, FriendshipRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('id', 'name', 'email', 'friends_count','avatar')
=======
        fields = ('id', 'name', 'email', 'friends_count', 'posts_count')
>>>>>>> 6880de426d0785f3a9e40d5e1e1c1e302cbf352f

class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by',)