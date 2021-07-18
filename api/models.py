from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	email = models.EmailField(verbose_name='email', max_length=254, unique=True)
	phone = models.CharField(null=True, max_length=250)
	self_description = models.CharField(null=True, blank=True, max_length=500)

	REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

	def __str__(self):
		return f'{self.id} {self.first_name} {self.last_name}'

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
	title = models.CharField(max_length=100, null=False, blank=False, unique=True)
	content = models.CharField(max_length=2000, null=False, blank=False)

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
	username = models.CharField(max_length=50, null=False, blank=False)
	content = models.CharField(max_length=2000, null=False, blank=False)

	def __str__(self):
		return self.username + ' on ' + self.post