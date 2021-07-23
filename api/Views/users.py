from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import User
from api.serializers import UserSerializer
from api.renderers import UserJSONRenderer

class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.select_related('self')
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, username, *args, **kwargs):
        # Try to retrieve the requested profile and throw an exception if the
        # profile could not be found.


        try:
            profile = User.objects.get(username=username)
        except Exception as e:
            raise serializers.ValidationError(e)

        imageURL = profile.imageURL
        profile_dict = profile.__dict__
        profile_dict['imageURL'] = imageURL

        serializer = self.serializer_class(
		profile_dict,
		context={
            'request': request
        })

        return Response(serializer.data, status=200)