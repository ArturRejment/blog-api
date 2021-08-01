from django.urls import path, re_path
from . import views
import api.Views.posts as PostView
import api.Views.comments as CommentsView
import api.Views.likes as LikesView
import api.Views.users as UsersView
import api.Views.tags as TagsView

urlpatterns = [
	path('', views.index, name='index'),
	path('post', PostView.PostView.as_view({'get': 'list', 'post':'create'}), name='all_posts'),
	path('top_posts', PostView.TopPostsView.as_view(), name="top_posts"),
	path('post/<int:id>', PostView.PostDetailView.as_view(), name='post'),
	path('post/<int:id>/comments', CommentsView.CommentDetailView.as_view({'get': 'list'}), name='post_comment'),
	path('post/<int:id>/likes', LikesView.viewLikesForPost, name='likes_for_post'),
	path('post/<int:id>/favorite', LikesView.ArticlesFavoriteAPIView.as_view(), name='like_post'),
	path('tags', TagsView.TagListView.as_view(), name='tags'),
	path('top_users', UsersView.TopUsersAPIView.as_view(), name='top_users'),
	re_path(r'^comment/(?P<id>[0-9]+)/favorite$', LikesView.CommentsFavoriteAPIView.as_view(), name='like_comment'),
	re_path(r'^user/(?P<username>[0-9-a-z-A-Z]+)$', UsersView.UserRetrieveAPIView.as_view(), name='profile'),
]
