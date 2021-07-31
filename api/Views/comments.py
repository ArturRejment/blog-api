from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework import generics, mixins, viewsets

import api.models as ApiModels
import api.serializers as ApiSerializers
import api.renderers as ApiRenderers


class CommentDetailView(mixins.ListModelMixin, viewsets.GenericViewSet):
	""" CDUD functionality for specific comments """
	renderer_classes = (ApiRenderers.CommentJSONRenderer,)
	serializer_classes = ApiSerializers.CommentSerializer

	def list(self, request, **kwargs):
		""" Return comments for specific post """

		serializer_context = {'request': request}
		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception:
			raise NotFound('Post with this id does not exist')
		comments = self.paginate_queryset(post.comment_set.all())
		serializer = self.serializer_classes(comments, context=serializer_context, many=True)
		return self.get_paginated_response(serializer.data)

	def post(self, request, **kwargs):
		""" Create comment for specific post """
		serializer_context = {
			'author': request.user,
			'request': request
		}
		if not request.user.is_authenticated:
			raise NotFound('User must be authenticated')
		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')
		serializer = ApiSerializers.CommentSerializer(
			data={
				'post': post.id,
				'content': request.data.get('content')
			}, context=serializer_context
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=200)
