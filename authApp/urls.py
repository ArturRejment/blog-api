from django.urls import path, include
from authApp import views

urlpatterns = [
	path('', include('djoser.urls')),
	path('', include('djoser.urls.authtoken')),
]
