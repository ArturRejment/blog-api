from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError

import api.models as ApiModels
import api.serializers as ApiSerializers

class CommentView(APIView):
	""" CRUD functionality for comments """

	def get(self, request):
		""" Returns all comments """

		comments = ApiModels.Comment.objects.all()
		serializer = ApiSerializers.CommentSerializer(comments, many=True)
		return Response(serializer.data, status=200)

class CommentDetailView(APIView):
	""" CDUD functionality for specific comments """

	def get(self, request, **kwargs):
		""" Return comments for specific post """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise ValidationError(e)

		comments = post.comment_set.all()
		serializer = ApiSerializers.CommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request, **kwargs):
		""" Create comment for specific post """

		postID = kwargs['id']
		try:
			post = ApiModels.Post.objects.get(id=postID)
		except Exception as e:
			raise ValidationError(e)

		serializer = ApiSerializers.CommentSerializer(
			data={
				'post': postID,
				'username': request.data.get('username'),
				'content': request.data.get('content')
			}
		)

		if serializer.is_valid():
			serializer.save()
			return Response("Comment added!", status=200)
		else:
			raise ValidationError('Wrong data')