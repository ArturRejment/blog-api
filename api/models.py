from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	email = models.EmailField(verbose_name='email', max_length=254, unique=True)
	phone = models.CharField(null=True, max_length=250)
	self_description = models.CharField(null=True, blank=True, max_length=500)
	user_pic = models.ImageField(upload_to="user_pics", default="default.png", height_field=None, width_field=None, max_length=None)
	bio = models.TextField(blank=True)
	follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
	favorites = models.ManyToManyField('Post', related_name='favorited_by')

	REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

	@property
	def imageURL(self):
		try:
			url = 'http://127.0.0.1:7000/static' + self.user_pic.url
		except Exception:
			url = ''
		return url

	def __str__(self):
		return f'{self.id} {self.first_name} {self.last_name}'

	def follow(self, profile):
		"""Follow `profile` if we're not already following `profile`."""
		self.follows.add(profile)

	def unfollow(self, profile):
		"""Unfollow `profile` if we're already following `profile`."""
		self.follows.remove(profile)

	def is_following(self, profile):
		"""Returns True if we're following `profile`; False otherwise."""
		return self.follows.filter(id=profile.id).exists()

	def is_followed_by(self, profile):
		"""Returns True if `profile` is following us; False otherwise."""
		return self.followed_by.filter(id=profile.get('id')).exists()

	def favorite(self, article):
		"""Favorite `article` if we haven't already favorited it."""
		self.favorites.add(article)

	def unfavorite(self, article):
		"""Unfavorite `article` if we've already favorited it."""
		self.favorites.remove(article)

	def has_favorited(self, article):
		"""Returns True if we have favorited `article`; else False."""
		return self.favorites.filter(pk=article.pk).exists()

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
	title = models.CharField(max_length=100, null=False, blank=False, unique=True)
	content = models.CharField(max_length=2000, null=False, blank=False)
	image = models.ImageField(upload_to="post_pics", default="default.png", height_field=None, width_field=None, max_length=None)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	@property
	def imageURL(self):
		try:
			url = 'http://127.0.0.1:7000/static' + self.image.url
		except Exception:
			url = ''
		return url

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
	content = models.CharField(max_length=2000, null=False, blank=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)

	@property
	def number_of_likes(self):
		likes = self.commentlike_set.all()
		return likes.count()

	def __str__(self):
		return f'{self.author.username} on  {self.post}'


class CommentLike(models.Model):
	user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, null=False, blank=False, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user} likes {self.comment}'