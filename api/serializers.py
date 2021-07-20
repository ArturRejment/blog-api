from rest_framework import serializers
import api.models as ApiModels
from djoser.serializers import UserCreateSerializer, UserSerializer

class UserSerializer(UserSerializer):
	class Meta(UserSerializer.Meta):
		model = ApiModels.User
		fields = ['username', 'first_name', 'last_name', 'imageURL']

class PostSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	class Meta:
		model = ApiModels.Post
		fields = ['id', 'author', 'title', 'content', 'number_of_likes', 'imageURL']

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Comment
		fields = ['id', 'post', 'username', 'content']

class PostLikeSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = ApiModels.PostLike
		fields = ['user']

class CommentLikeSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = ApiModels.CommentLike
		fields = ['user']