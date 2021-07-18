from django.test import TestCase
from rest_framework.test import APITestCase
import api.models as ApiModels

class TestPostEndpoints(APITestCase):
	""" Testing some basic Post Endpoints """

	def setUp(self):
		""" Set up Post tests """

		# Create one user for tests
		self.user1 = ApiModels.User.objects.create(
			username = 'test',
			first_name='Test',
			last_name='Test',
			email='test@gmail.com'
		)

		# Create new post
		self.post1 = ApiModels.Post.objects.create(
			author=self.user1,
			title='New',
			content='Hi'
		)

	def test_post_POST(self):
		""" Test POST method """

		response = self.client.post(
			'/post/',
			{
				'author': self.user1.id,
				'title': 'New tech',
				'content': 'Hello'
			},
			headers={
				'Content-Type':'application/x-www-form-urlencoded'
			}
		)

		self.assertEquals(response.status_code, 201)

	def test_post_GET(self):
		""" Test GET method """

		response = self.client.get(
			'/post/'
		)

		# There should be no posts
		self.assertEquals(response.status_code, 200)
		self.assertEquals(len(response.data), 1)

		# Create new post
		self.test_post_POST()

		response = self.client.get(
			'/post/'
		)

		# There should be one post
		self.assertEquals(response.status_code, 200)
		self.assertEquals(len(response.data), 2)

	def test_post_PUT(self):
		""" Test PUT method """

		response = self.client.put(
			f'/post/{self.post1.id}/',
			{
				'author': self.user1.id,
				'title': 'New technology',
				'content': 'Hello there'
			},
			headers={
				'Content-Type':'application/x-www-form-urlencoded'
			}
		)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.data.get('title'), 'New technology')

	def test_post_DELETE(self):
		""" Test DELETE method """

		response = self.client.delete(
			f'/post/{self.post1.id}/',
		)

		self.assertEquals(response.status_code, 200)
