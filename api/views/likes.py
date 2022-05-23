from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from api.models import Post, Comment
from api.serializers import PostSerializer, CommentSerializer
from api.renderers import PostJSONRenderer, CommentJSONRenderer


class ArticlesFavoriteAPIView(APIView):
    """ Views for favorite and unfavorite specific post """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (PostJSONRenderer,)
    serializer_class = PostSerializer

    def delete(self, request, id: int = None):
        """ Remove post from favorites """
        user = self.request.user
        serializer_context = {'request': request}
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        user.unfavorite(post)
        serializer = self.serializer_class(post, context=serializer_context)
        return Response(serializer.data, status=200)

    def post(self, request, id: int = None):
        """ Add post to favorites """
        user = self.request.user
        serializer_context = {'request': request}
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise NotFound('An post with this id was not found.')

        user.favorite(post)
        serializer = self.serializer_class(post, context=serializer_context)
        return Response(serializer.data, status=201)


class CommentsFavoriteAPIView(APIView):
    """ Views for favorite and unfavorite specific comment """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def delete(self, request, id: id = None):
        """ Remove comment from favorites """

        user = self.request.user
        serializer_context = {'request': request}
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound('An post with this id was not found.')

        user.unfavorite_comment(comment)
        serializer = self.serializer_class(comment, context=serializer_context)
        return Response(serializer.data, status=200)

    def post(self, request, id: int = None):
        """ Add comment to favorites """

        user = self.request.user
        serializer_context = {'request': request}
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound('An comment with this id was not found.')

        user.favorite_comment(comment)
        serializer = self.serializer_class(comment, context=serializer_context)
        return Response(serializer.data, status=201)
