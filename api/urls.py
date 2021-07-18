from django.urls import path
from . import views
import api.Views.posts as PostViews

urlpatterns = [
	path('', views.index, name='index'),
	path('post/', PostViews.PostView.as_view(), name='post'),
]
