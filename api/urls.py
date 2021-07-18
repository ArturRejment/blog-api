from django.urls import path
from . import views
import api.Views.posts as PostView
import api.Views.comments as CommentsView

urlpatterns = [
	path('', views.index, name='index'),
	path('post/', PostView.PostView.as_view(), name='all_posts'),
	path('post/<int:id>/', PostView.PostDetailView.as_view(), name='post'),
	path('post/<int:id>/comments/', CommentsView.CommentDetailView.as_view(), name='post_comment'),
	path('comments/', CommentsView.CommentView.as_view(), name='comments')
]
