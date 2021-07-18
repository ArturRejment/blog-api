from django.test import TestCase
from rest_framework.test import APITestCase
import api.models as ApiModels

class TestPostEndpoints(APITestCase):
	""" Testing some basic Post Endpoints """

	def setUp(self):
		user1 = ApiModels.User.objects.create(
			username = 'test',
			first_name='Test',
			last_name='Test',
			email='test@gmail.com'
		)

	def test_post_POST(self):

		response = self.client.post(
			'/post/',
			{
				'author': 2,
				'title': 'New tech',
				'content': 'Hello'
			},
			headers={
				'Content-Type':'application/x-www-form-urlencoded'
			}
		)

		self.assertEquals(response.status_code, 201)