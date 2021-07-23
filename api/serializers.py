from rest_framework import serializers
import api.models as ApiModels
from djoser.serializers import UserCreateSerializer, UserSerializer

class UserSerializer(UserSerializer):
	bio = serializers.CharField(allow_blank=True, required=False)
	following = serializers.SerializerMethodField()
	class Meta(UserSerializer.Meta):
		model = ApiModels.User
		fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'imageURL', 'following']

	# Check if currently logged user is following specific User
	def get_following(self, instance):
		request = self.context.get('request', None)

		if request is None:
			return False

		if not request.user.is_authenticated:
			return False

		follower = request.user
		followee = instance

		return follower.is_following(followee)

class PostSerializer(serializers.ModelSerializer):
	""" Post serializer """
	author = UserSerializer(read_only=True)
	favorited = serializers.SerializerMethodField()
	favoritesCount = serializers.SerializerMethodField(
	    method_name='get_favorites_count'
    )
	class Meta:
		model = ApiModels.Post
		fields = ['id', 'author', 'image', 'title', 'content', 'imageURL', 'favorited', 'favoritesCount']

		# Specify only read fields - serializer will display them, but they are not
		# required to create object
		read_only_fields = ('author',)

		# According to the documentation this is new way to specify only-write fields
		# That means, this fields are required to create object but will not be displayed
		extra_kwargs = {
			'image': {'write_only': True}
		}

	def create(self, validated_data):
		""" Method to create Post object using serializer """
		# Get post author from the context
		author = self.context.get('author', None)
		post = ApiModels.Post.objects.create(author=author, **validated_data)
		return post

	def get_favorited(self, instance):
		request = self.context.get('request', None)

		if request is None:
			return False

		if not request.user.is_authenticated:
			return False

		return request.user.has_favorited(instance)

	def get_favorites_count(self, instance):
		return instance.favorited_by.count()



class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApiModels.Comment
		fields = ['id', 'post', 'username', 'content']


class CommentLikeSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = ApiModels.CommentLike
		fields = ['user']