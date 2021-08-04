import json

from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db import connection
from rest_framework.pagination import PageNumberPagination

from api.models import User, Post
from api.serializers import UserSerializer
from api.renderers import UserJSONRenderer


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, username, *args, **kwargs):
        """ Try to retrieve the requested profile and throw an exception if the
         profile could not be found. """
        try:
            profile = User.objects.get(username=username)
        except Exception:
            raise NotFound('User with this username does not exist.')

        imageURL = profile.imageURL
		# Renderer needs the dictionary object so send instance.__dict__
        profile_dict = profile.__dict__
		# Set imageURL in the dictionary
        profile_dict['imageURL'] = imageURL

        serializer = self.serializer_class(
		profile_dict,
		context={
            'request': request
        })

        return Response(serializer.data, status=200)


class TopUsersAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request):
        """ Returns 3 top users based on number of created posts """
        serializer_context = {'request': request}
        query_data = None
        # Perform raw SQL query in order to get 3 most popular authors
        with connection.cursor() as cursor:
            cursor.execute('SELECT count(api_post.id) as counting, api_post.author_id \
                            FROM api_post \
                            GROUP BY api_post.author_id \
                            ORDER BY counting DESC \
                            LIMIT 3')
            query_data = cursor.fetchall()
        # New list for users data
        new_json = []
        # Loop through returned tuples
        for index in query_data:
            # Try to fetch User
            try:
                user = User.objects.get(id=index[1])
            except Exception as e:
                raise NotFound(f'User with id {index[1]} was not found')
            # Append serialized user to the array
            new_json.append(self.serializer_class(user).data)
        # Return serialized data in proper format
        return Response({'users':new_json}, status=200)


class FollowUserView(APIView):

    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def post(self, request, username=None):
        """ Follow user specified by username """

        serializer_context = {'request': request}
        follower = request.user
        try:
            followee = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('User with this username does not exist')

        follower.follow(followee)
        serializer = self.serializer_class(followee, context=serializer_context)
        return Response(serializer.data, status=200)

    def delete(self, request, username=None):
        """ Unfollow user specified by username """

        serializer_context = {'request': request}
        follower = request.user
        try:
            followee = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('User with this username does not exist')

        follower.unfollow(followee)
        serializer = self.serializer_class(followee, context=serializer_context)
        return Response(serializer.data, status=200)

