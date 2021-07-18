from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

import api.models as ApiModels
import api.serializers as ApiSerializers


class PostView(APIView):
	""" Basic POST, GET, PUT and DELETE methods for Post model """

	def post(self, request):
		""" Create new Post """

		serializer = ApiSerializers.PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response("Post created successfully", status=201)
		else:
			return Response(serializer.errors, status=422)

	def get(self, request):
		""" Return set of all posts """

		posts = ApiModels.Post.objects.all()
		serializer = ApiSerializers.PostSerializer(posts, many=True)
		return Response(serializer.data, status=200)

class PostDetailView(APIView):
	""" CRUD for specific post """

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