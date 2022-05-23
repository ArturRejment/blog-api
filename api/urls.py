from django.urls import path, re_path
from . import views
import api.views.posts as PostView
import api.views.comments as CommentsView
import api.views.likes as LikesView
import api.views.users as UsersView
import api.views.tags as TagsView

urlpatterns = [
	path('', views.index, name='index'),
	path('post', PostView.PostView.as_view({'get': 'list', 'post':'create'}), name='all_posts'),
	path('top_posts', PostView.TopPostsView.as_view(), name="top_posts"),
	path('post/<int:id>', PostView.PostDetailView.as_view(), name='post'),
	path('post/<int:id>/comments', CommentsView.CommentDetailView.as_view({'get': 'list'}), name='post_comment'),
	path('post/<int:id>/favorite', LikesView.ArticlesFavoriteAPIView.as_view(), name='like_post'),
	path('tags', TagsView.TagListView.as_view(), name='tags'),
	path('top_users', UsersView.TopUsersAPIView.as_view(), name='top_users'),
	path('comment/<int:id>', CommentsView.DeleteCommentView.as_view({'delete':'destroy'}), name='comment_delete'),
	re_path(r'^comment/(?P<id>[0-9]+)/favorite$', LikesView.CommentsFavoriteAPIView.as_view(), name='like_comment'),
	re_path(r'^user/(?P<username>[0-9-a-z-A-Z]+)$', UsersView.UserRetrieveAPIView.as_view(), name='profile'),
	path('user/<str:username>/fav_posts', PostView.FavoritePostsView.as_view({'get': 'list'}), name='posts_favorited_by'),
	path('user/<str:username>/fav_comments', CommentsView.FavoritedCommentsView.as_view({'get': 'list'}), name='posts_favorited_by'),
	path('user/<str:username>/follow', UsersView.FollowUserView.as_view(), name='follow_user'),
]
