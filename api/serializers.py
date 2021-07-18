from rest_framework import serializers
import api.models as ApiModels

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Post
		fields = ['id', 'author', 'title', 'content']
