from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework import generics, mixins, viewsets

import api.models as ApiModels
import api.serializers as ApiSerializers
import api.renderers as ApiRenderers


class CommentDetailView(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
	""" CD** functionality for specific comments """
	renderer_classes = (ApiRenderers.CommentJSONRenderer,)
	serializer_classes = ApiSerializers.CommentSerializer

	def list(self, request, **kwargs):
		""" Returns all comments for specific post """

		# Serializer context required for JSONRenderer
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

		# Serializer context required for JSONRenderer
		serializer_context = {
			'author': request.user,
			'request': request
		}
		# Check if user is authenticated
		if not request.user.is_authenticated:
			raise NotFound('User must be authenticated')
		postID = kwargs['id']
		# Fetch specific post
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise NotFound('Post with this id does not exist')
		# Create a comment for fetched post
		serializer = ApiSerializers.CommentSerializer(
			data={
				'post': post.id,
				'content': request.data.get('content')
			}, context=serializer_context
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=200)


class DeleteCommentView(mixins.DestroyModelMixin, viewsets.GenericViewSet):

	def destroy(self, request, *args, **kwargs):
		""" Delete specific comment """
		user = request.user
		commentID = kwargs['id']
		try:
			comment = ApiModels.Comment.objects.get(id=commentID)
		except ApiModels.Comment.DoesNotExist:
			raise NotFound('Comment with this id does not exist')

		if comment.author != user:
			raise ValidationError('You have not privilages to delete this comment.')

		comment.delete()
		return Response({'Comment': 'Comment deleted successfully'}, status=200)


class FavoritedCommentsView(mixins.ListModelMixin, viewsets.GenericViewSet):
	serializer_class = ApiSerializers.CommentSerializer
	renderer_classes = (ApiRenderers.CommentJSONRenderer,)

	def list(self, request, **kwargs):
		""" List of comments favorited by specific user """
		serializer_context = {'request': request}
		# Fetch the user
		try:
			user = ApiModels.User.objects.get(username=kwargs["username"])
		except ApiModels.User.DoesNotExist:
			raise NotFound('User with this username does not exist')

		comments = ApiModels.Comment.objects.filter(favorited_comment=user)
		paginated_comments = self.paginate_queryset(comments)
		serializer = self.serializer_class(paginated_comments, context=serializer_context, many=True)
		return self.get_paginated_response(serializer.data)
