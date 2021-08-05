from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, mixins, viewsets
from rest_framework.exceptions import NotFound
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from django.views.generic import DetailView

import api.models as ApiModels
import api.serializers as ApiSerializers
import api.renderers as ApiRenderers
from analytics.mixins import ObjectViewedMixin
from analytics.signals import object_viewed_signal


class PostView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
	""" Basic CR** methods for Post model """

	lookup_field = 'title'
	queryset = ApiModels.Post.objects.select_related('author').prefetch_related('tags')
	parser_classes = [MultiPartParser, FormParser]
	renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_classes = ApiSerializers.PostSerializer

	def get_queryset(self):
		queryset = self.queryset
		author = self.request.query_params.get('author', None)
		tag = self.request.query_params.get('tag', None)
		if author is not None:
			queryset = queryset.filter(Q(author__username__in=[author]))
		if tag is not None:
			queryset = queryset.filter(Q(tags__tag=tag))
		return queryset

	@permission_classes([IsAuthenticated])
	def create(self, request):
		""" Create new Post """

		serializer_context = {
			'author': request.user,
			'request': request
		}
		serializer = self.serializer_classes(
			data=request.data, context=serializer_context
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=201)

	def list(self, request):
		""" Return set of all posts """

		serializer_context = {'request': request}
		posts = self.paginate_queryset(self.get_queryset())
		serializer = self.serializer_classes(posts, context=serializer_context, many=True)
		return self.get_paginated_response(serializer.data)


class FavoritedPostsView(mixins.ListModelMixin, viewsets.GenericViewSet):
	serializer_class = ApiSerializers.PostSerializer
	renderer_classes = (ApiRenderers.PostJSONRenderer,)

	def list(self, request, **kwargs):
		""" List of posts favorited by specific user """
		serializer_context = {'request': request}
		# Fetch the user
		try:
			user = ApiModels.User.objects.get(username=kwargs['username'])
		except ApiModels.User.DoesNotExist:
			raise NotFound('User with this username does not exist')
		posts = ApiModels.Post.objects.filter(favorited_by=user)
		paginated_posts = self.paginate_queryset(posts)
		serializer = self.serializer_class(paginated_posts, context=serializer_context, many=True)
		return self.get_paginated_response(serializer.data)


class TopPostsView(APIView):
	""" Returns 3 most liked posts """
	# renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_class = ApiSerializers.PostSerializer

	def get(self, request):
		""" Get 3 most liked posts """
		serializer_context = {'request': request}
		query_data = None
		# Perform raw SQL query in order to get 3 most popular posts
		with connection.cursor() as cursor:
			cursor.execute('SELECT post_id, count(user_id) \
							FROM api_user_favorites \
							GROUP BY post_id \
							ORDER BY count(user_id) DESC \
							LIMIT 3')
			query_data = cursor.fetchall()
		# New list for posts data
		new_json = []
		# Loop through returned tuples
		for index in query_data:
			# Try to fetch Posts
			try:
				post = ApiModels.Post.objects.get(id=index[0])
			except Exception as e:
				raise NotFound(f'Post with id {index[1]} was not found')
			# Append serialized user to the array
			new_json.append(self.serializer_class(post).data)
		# Return serialized data in proper format
		return Response({'posts':new_json}, status=200)


class PostDetailView(APIView):
	""" *RUD for specific post """
	renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_classes = ApiSerializers.PostSerializer

	def get(self, request, *args, **kwargs):
		""" Get specific post """
		serializer_context = {'request': self.request}

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')
		# Serialize post
		serializer = self.serializer_classes(post, context=serializer_context)
		# Use signal to create ObjectViewed
		object_viewed_signal.send(post.__class__, instance=post, request=request)
		return Response(serializer.data, status=200)

	@permission_classes([IsAuthenticated])
	def patch(self, request, **kwargs):
		""" Change existing post """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')
		# Check if currently logged user is an author of this post
		if post.author != request.user:
			raise NotFound('You are not authorized to edit this post!')
		# Update post
		serializer = ApiSerializers.PostSerializer(instance=post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=200)
		else:
			return Response(serializer.errors, status=422)

	@permission_classes([IsAuthenticated])
	def delete(self, request, **kwargs):
		""" Delete post """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')
		# Check if currently logged user is an author of this post
		if post.author != request.user:
			raise NotFound('You are not authorized to edit this post!')
		# Try to delete this post
		try:
			post.delete()
		except Exception as e:
			return Response({'error':e})
		else:
			return Response({'post':'deleted'}, status=200)
