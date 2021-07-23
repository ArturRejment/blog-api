from django.urls import path, re_path
from . import views
import api.Views.posts as PostView
import api.Views.comments as CommentsView
import api.Views.likes as LikesView
import api.Views.users as UsersView

urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^(?P<username>[0-9-a-z-A-Z]+)/$', UsersView.UserRetrieveAPIView.as_view(), name='profile'),
	path('post/', PostView.PostView.as_view({'get': 'list', 'post':'create'}), name='all_posts'),
	path('post/<int:id>/', PostView.PostDetailView.as_view(), name='post'),
	path('post/<int:id>/comments/', CommentsView.CommentDetailView.as_view(), name='post_comment'),
	path('post/<int:id>/likes/', LikesView.viewLikesForPost, name='likes_for_post'),
	path('post/<int:id>/like/', LikesView.likePost, name='like_post'),
	path('comments/', CommentsView.CommentView.as_view(), name='comments'),
	path('comment/<int:id>/like/', LikesView.likeComment, name='like_comment'),
]
