from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
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
