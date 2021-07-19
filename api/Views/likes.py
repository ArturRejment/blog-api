from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import ValidationError

import api.models as ApiModels
import api.serializers as ApiSerializers

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
