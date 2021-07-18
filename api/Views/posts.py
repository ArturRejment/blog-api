from rest_framework.views import APIView
from rest_framework.response import Response

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