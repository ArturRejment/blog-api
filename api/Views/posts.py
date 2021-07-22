from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, mixins, viewsets

import api.models as ApiModels
import api.serializers as ApiSerializers
import api.renderers as ApiRenderers


class PostView(
				mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

	""" Basic POST, GET, PUT and DELETE methods for Post model """
	parser_classes = [MultiPartParser, FormParser]
	renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_classes = ApiSerializers.PostSerializer

	@permission_classes([IsAuthenticated])
	def post(self, request):
		""" Create new Post """

		serializer = ApiSerializers.PostCreateSerializer(
			data=request.data
		)
		if serializer.is_valid():
			serializer.save()
			return Response("Post created successfully", status=201)
		else:
			return Response(serializer.errors, status=422)

	def list(self, request):
		""" Return set of all posts """
		serializer_context = {'request', request}

		posts = self.paginate_queryset(ApiModels.Post.objects.all())
		serializer = ApiSerializers.PostSerializer(posts, context=serializer_context, many=True)
		return self.get_paginated_response(serializer.data)

class PostDetailView(APIView):
	""" CRUD for specific post """
	renderer_classes = (ApiRenderers.PostJSONRenderer,)
	serializer_classes = ApiSerializers.PostSerializer

	def get(self, request, **kwargs):
		""" Get specific post """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise ValidationError(e)

		serializer = ApiSerializers.PostSerializer(post)
		return Response(serializer.data, status=200)

	def put(self, request, **kwargs):
		""" Change existing post

			Required params:
			@param1 - postID """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise ValidationError(e)

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
			raise ValidationError(e)

		try:
			post.delete()
		except Exception as e:
			return Response(e)
		else:
			return Response("Post deleted", status=200)