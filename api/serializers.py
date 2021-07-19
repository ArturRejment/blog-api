from rest_framework import serializers
import api.models as ApiModels

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Post
		fields = ['id', 'author', 'title', 'content', 'number_of_likes']

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Comment
		fields = ['id', 'post', 'username', 'content']

class PostLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.PostLike
		fields = ['user']

class CommentLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.CommentLike
		fields = ['user']