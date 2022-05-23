from django.urls import reverse , resolve
from rest_framework import status
from rest_framework.test import APITestCase
from api.views.posts import PostView, PostDetailView

class PostTests(APITestCase):

	def setUp(self):
		pass

	def test_post_url(self):
		url = 'all_posts'
		reversed_url = reverse(url)
		response = self.client.get('/post')
		# self.assertEqual(resolve(reversed_url).func, )
		self.assertEqual(response.status_code, 200)