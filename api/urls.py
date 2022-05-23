from django.urls import path, re_path

from api.views.posts import TopPostsView, PostView, PostDetailView, FavoritePostsView
from api.views.comments import CommentDetailView, DeleteCommentView, FavoritedCommentsView
from api.views.likes import ArticlesFavoriteAPIView, CommentsFavoriteAPIView
from api.views.users import TopUsersAPIView, UserRetrieveAPIView, FollowUserView
from api.views.tags import TagListView

urlpatterns = [
    path('post', PostView.as_view({'get': 'list', 'post':'create'}), name='all_posts'),
    path('top_posts', TopPostsView.as_view(), name="top_posts"),
    path('post/<int:id>', PostDetailView.as_view(), name='post'),
    path('user/<str:username>/fav_posts', FavoritePostsView.as_view({'get': 'list'}), name='posts_favorited_by'),

    path('post/<int:id>/comments', CommentDetailView.as_view({'get': 'list'}), name='post_comment'),
    path('comment/<int:id>', DeleteCommentView.as_view({'delete':'destroy'}), name='comment_delete'),
    path('user/<str:username>/fav_comments', FavoritedCommentsView.as_view({'get': 'list'}), name='posts_favorited_by'),

    path('post/<int:id>/favorite', ArticlesFavoriteAPIView.as_view(), name='like_post'),
    re_path(r'^comment/(?P<id>[0-9]+)/favorite$', CommentsFavoriteAPIView.as_view(), name='like_comment'),

    path('top_users', TopUsersAPIView.as_view(), name='top_users'),
    re_path(r'^user/(?P<username>[0-9-a-z-A-Z]+)$', UserRetrieveAPIView.as_view(), name='profile'),
    path('user/<str:username>/follow', FollowUserView.as_view(), name='follow_user'),

    path('tags', TagListView.as_view(), name='tags'),
]
