from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework import mixins, viewsets

from api.models import Post, User, Comment
from api.serializers import CommentSerializer, PostSerializer
from api.renderers import CommentJSONRenderer, PostJSONRenderer


class CommentDetailView(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """ CD** functionality for specific comments """
    renderer_classes = (CommentJSONRenderer,)
    serializer_classes = CommentSerializer

    def list(self, request, **kwargs):
        """ Returns all comments for specific post """
        serializer_context = {'request': request}
        post_id = kwargs.get('id', 0)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound('Post with this id does not exist')

        comments = self.paginate_queryset(post.comment_set.all())
        serializer = self.serializer_classes(comments, context=serializer_context, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, **kwargs):
        """ Create comment for specific post """
        serializer_context = {
            'author': request.user,
            'request': request
        }

        if not request.user.is_authenticated:
            raise NotFound('User must be authenticated')

        post_id = kwargs.get('id', 0)
        # Fetch specific post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound('Post with this id does not exist')

        # Create a comment for fetched post
        serializer = CommentSerializer(
            data={
                'post': post.id,
                'content': request.data.get('content')
            },
            context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class DeleteCommentView(mixins.DestroyModelMixin, viewsets.GenericViewSet):

    def destroy(self, request, *args, **kwargs):
        """ Delete specific comment """
        user = request.user
        comment_id = kwargs.get('id', 0)
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound('Comment with this id does not exist')

        if comment.author != user:
            raise ValidationError('You have not privileges to delete this comment.')

        comment.delete()
        return Response({'Comment': 'Comment deleted successfully'}, status=200)


class FavoritedCommentsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    renderer_classes = (CommentJSONRenderer,)

    def list(self, request, **kwargs):
        """ List of comments favorited by specific user """
        serializer_context = {'request': request}

        # Fetch the user
        try:
            user = User.objects.get(username=kwargs["username"])
        except User.DoesNotExist:
            raise NotFound('User with this username does not exist')

        comments = Comment.objects.filter(favorited_comment=user)
        paginated_comments = self.paginate_queryset(comments)
        serializer = self.serializer_class(paginated_comments, context=serializer_context, many=True)
        return self.get_paginated_response(serializer.data)
