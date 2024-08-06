from rest_framework import serializers
from .models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email", "date_of_birth"]

class AccountSerializerUserPassowrd(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email", "date_of_birth", "username", "password"]

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "status"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "author", "text", "image", "datetime", "like_count", "comment_count"]