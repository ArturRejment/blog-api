from rest_framework import serializers
import api.models as ApiModels
from djoser.serializers import UserCreateSerializer, UserSerializer
from .relations import TagRelatedField


class UserSerializer(UserSerializer):
	bio = serializers.CharField(allow_blank=True, required=False)
	following = serializers.SerializerMethodField()
	class Meta(UserSerializer.Meta):
		model = ApiModels.User
		fields = ['id', 'username', 'first_name', 'last_name', 'bio',
				  'imageURL', 'github_link', 'linkedin_link', 'facebook_link', 'following']

	def get_following(self, instance):
		""" Check if currently logged user is following specific User """
		request = self.context.get('request', None)
		if request is None:
			return False
		if not request.user.is_authenticated:
			return False
		follower = request.user
		followee = instance
		return follower.is_following(followee)


class PostSerializer(serializers.ModelSerializer):
	""" Serialize Post object """
	author = UserSerializer(read_only=True)
	favorited = serializers.SerializerMethodField()
	tagList = TagRelatedField(many=True, required=False, source='tags')
	createdAt = serializers.SerializerMethodField(method_name='get_created_at')
	next_post_id = serializers.SerializerMethodField(method_name='get_next_post')
	previous_post_id = serializers.SerializerMethodField(method_name='get_prev_post')

	class Meta:
		model = ApiModels.Post
		fields = ['id', 'author', 'image', 'title', 'description', 'content',
				  'imageURL', 'createdAt', 'next_post_id', 'previous_post_id', 'tagList', 'favorited', 'favorites_count']

		# Specify read_only fields - serializer will display them, but they are not
		# required to create object
		read_only_fields = ('author',)

		# According to the documentation this is new way to specify write_only fields
		# That means, theses fields are required to create object but will not be displayed
		extra_kwargs = {
			'image': {'write_only': True}
		}

	def create(self, validated_data):
		""" Method to create Post object using serializer """
		# Get post author from the context
		author = self.context.get('author', None)
		tags = validated_data.pop('tags', [])
		post = ApiModels.Post.objects.create(author=author, **validated_data)
		# Add tags to the created post
		if len(tags) > 0:
			tags = str(tags[0]).split(',')
		for tag in tags:
			tag = tag.strip()
			try:
				qs = ApiModels.Tag.objects.get_or_create(tag=tag)
			except:
				continue
			post.tags.add(qs[0])
		return post

	def get_favorited(self, instance):
		""" Returs True if currently logged User has this Post in favorites;
		 	Returns False otherwise, or if the User is not logged """
		request = self.context.get('request', None)
		if request is None:
			return False
		if not request.user.is_authenticated:
			return False
		return request.user.has_favorited(instance)

	def get_created_at(self, instance):
		return instance.created_at.isoformat()

	def get_next_post(self, instance):
		""" Return id of next post in the database, if exists """
		next_post = ApiModels.Post.objects.filter(id__gt=instance.id).order_by('id').first()
		if next_post is not None:
			return next_post.id
		else:
			return None

	def get_prev_post(self, instance):
		""" Return id of previous post in the database, if exists """
		next_post = ApiModels.Post.objects.filter(id__lt=instance.id).order_by('-id').first()
		if next_post is not None:
			return next_post.id
		else:
			return None


class CommentSerializer(serializers.ModelSerializer):
	author = UserSerializer(read_only=True)
	favorited = serializers.SerializerMethodField()
	favorites_count = serializers.SerializerMethodField(method_name='get_favorites_comment_count')
	class Meta:
		model = ApiModels.Comment
		fields = ['id', 'post', 'author', 'content', 'favorited', 'favorites_count']
		read_only_fields = ('author',)

	def create(self, validated_data):
		""" Method to create Comment object using serializer """
		# Get comment author from the context
		author = self.context.get('author', None)
		comment = ApiModels.Comment.objects.create(author=author, **validated_data)
		return comment

	def get_favorited(self, instance):
		""" Returs True if currently logged User has this Comment in favorites;
		 	Returns False otherwise, or if the User is not logged """
		request = self.context.get('request', None)
		if request is None:
			return False
		# Check if user is authenticated
		if not request.user.is_authenticated:
			return False
		return request.user.has_favorited_comment(instance)

	def get_favorites_comment_count(self, instance):
		"""Return number of people who favorited this comment """
		return instance.favorited_comment.count()


class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = ApiModels.Tag
		fields = ['tag']