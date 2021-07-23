from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

import api.models as ApiModels
import api.serializers as ApiSerializers
from api.renderers import PostJSONRenderer

class ArticlesFavoriteAPIView(APIView):
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likePost(request, **kwargs):
	user = request.user
	postID = kwargs['id']
	try:
		post = ApiModels.Post.objects.get(id=postID)
	except Exception as e:
		raise ValidationError(e)

	for i, element in enumerate(user.postlike_set.all()):
		if post == element.post:
			raise ValidationError({'User': 'User already likes this post'}, code=422)

	ApiModels.PostLike.objects.create(
		user=user,
		post=post
	)

	return Response("Post liked", status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likeComment(request, **kwargs):
	""" Allows to like specific comment by currently logged user """
	user = request.user
	commentID = kwargs['id']
	try:
		comment = ApiModels.Comment.objects.get(id=commentID)
	except Exception as e:
		raise ValidationError(e)

	for i, element in enumerate(user.commentlike_set.all()):
		if comment == element.comment:
			raise ValidationError({'User': 'User already likes this comment'}, code=422)

	ApiModels.CommentLike.objects.create(
		user=user,
		comment=comment
	)

	return Response("Comment liked", status=200)
