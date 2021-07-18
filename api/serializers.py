from rest_framework import serializers
import api.models as ApiModels

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Post
		fields = ['id', 'author', 'title', 'content']

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Comment
		fields = ['id', 'post', 'username', 'content']