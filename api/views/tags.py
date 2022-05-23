from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import Tag
from api.serializers import TagSerializer


class TagListView(generics.ListAPIView):
	queryset = Tag.objects.all()
	pagination_class = None
	permission_classes = (AllowAny,)
	serializer_class = TagSerializer

	def list(self, request) -> Response:
		serializer_data = self.get_queryset()
		serializer = self.serializer_class(serializer_data, many=True)

		return Response({'tags':serializer.data}, status=200)
