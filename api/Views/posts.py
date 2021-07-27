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

import api.models as ApiModels
import api.serializers as ApiSerializers
import api.renderers as ApiRenderers


class PostView(
				mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

	""" Basic CR** methods for Post model """
	parser_classes = [MultiPartParser, FormParser]
	renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_classes = ApiSerializers.PostSerializer

	def get_queryset(self):
		queryset = ApiModels.Post.objects.all()

		author = self.request.query_params.get('author', None)
		tag = self.request.query_params.get('tag', None)

		if author is not None:
			# author = author.split(",")
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

		serializer_data = {
			'title': request.data.get('title'),
				'content': request.data.get('content', None),
				'image': request.data.get('image', None)
		}

		serializer = self.serializer_classes(
			data=serializer_data, context=serializer_context
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

class PostDetailView(APIView):
	""" *RUD for specific post """
	renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_classes = ApiSerializers.PostSerializer

	def get(self, request, **kwargs):
		""" Get specific post """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')

		serializer = self.serializer_classes(post)
		return Response(serializer.data, status=200)

	def put(self, request, **kwargs):
		""" Change existing post

			Required params:
			@param1 - postID """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')

		serializer = ApiSerializers.PostSerializer(instance=post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=200)
		else:
			return Response(serializer.errors, status=422)

	def delete(self, request, **kwargs):
		""" Delete post

			Required params:
			@param1 - postID"""

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')

		try:
			post.delete()
		except Exception as e:
			return Response(e)
		else:
			return Response("Post deleted", status=200)