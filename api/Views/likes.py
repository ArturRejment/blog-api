from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

import api.models as ApiModels
import api.serializers as ApiSerializers
from api.renderers import PostJSONRenderer, CommentJSONRenderer

class ArticlesFavoriteAPIView(APIView):
	""" Views for favorite and unfavorite specific post """
	permission_classes = (IsAuthenticated,)
	renderer_classes = (PostJSONRenderer,)
	serializer_class = ApiSerializers.PostSerializer

	def delete(self, request, id=None):
		user = self.request.user
		serializer_context = {'request': request}

		try:
			post = ApiModels.Post.objects.get(id=id)
		except post.DoesNotExist:
			raise NotFound('An article with this slug was not found.')

		user.unfavorite(post)

		serializer = self.serializer_class(post, context=serializer_context)

		return Response(serializer.data, status=200)

	def post(self, request, id=None):
		user = self.request.user
		serializer_context = {'request': request}

		try:
			post = ApiModels.Post.objects.get(id=id)
		except ApiModels.Post.DoesNotExist:
			raise NotFound('An post with this id was not found.')

		user.favorite(post)

		serializer = self.serializer_class(post, context=serializer_context)

		return Response(serializer.data, status=201)

class CommentsFavoriteAPIView(APIView):
	""" Views for favorite and unfavorite specific comment """
	permission_classes = (IsAuthenticated,)
	renderer_classes = (CommentJSONRenderer,)
	serializer_class = ApiSerializers.CommentSerializer

	def delete(self, request, id=None):
		user = self.request.user
		serializer_context = {'request': request}

		try:
			comment = ApiModels.Comment.objects.get(id=id)
		except ApiModels.Comment.DoesNotExist:
			raise NotFound('An post with this id was not found.')

		user.unfavorite_comment(comment)

		serializer = self.serializer_class(comment, context=serializer_context)

		return Response(serializer.data, status=200)

	def post(self, request, id=None):
		user = self.request.user
		serializer_context = {'request': request}

		try:
			comment = ApiModels.Comment.objects.get(id=id)
		except ApiModels.Comment.DoesNotExist:
			raise NotFound('An comment with this id was not found.')

		user.favorite_comment(comment)

		serializer = self.serializer_class(comment, context=serializer_context)

		return Response(serializer.data, status=201)


@api_view(['GET'])
def viewLikesForPost(request, **kwargs):
	""" View all people who liked this post """
	postID = kwargs['id']
	try:
		post = ApiModels.Post.objects.get(id = postID)
	except Exception as e:
		raise ValidationError(e)

	likes = post.postlike_set.all()
	serializer = ApiSerializers.PostLikeSerializer(likes, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def viewLikesForComment(request, **kwargs):
	""" View all people who liked this comment """
	commentID = kwargs['id']
	try:
		comment = ApiModels.Comment.objects.get(id=commentID)
	except Exception as e:
		raise ValidationError(e)

	likes = comment.commentlike_set.all()
	serializer = ApiSerializers.CommentLikeSerializer(likes, many=True)
	return Response(serializer.data)
