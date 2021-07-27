from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

import api.models as ApiModels
# Create your views here.

@api_view(['GET'])
def index(request):
	posts = ApiModels.Post.objects.all()
	comments = ApiModels.Comment.objects.all()
	json = {'Blog Api'}
	return Response(json)
