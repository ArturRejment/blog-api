from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	email = models.EmailField(verbose_name='email', max_length=254, unique=True)
	phone = models.CharField(null=True, blank=True, max_length=250)
	self_description = models.CharField(null=True, blank=True, max_length=500)
	user_pic = models.ImageField(upload_to="user_pics", default="default.png", height_field=None, width_field=None, max_length=None)
	bio = models.TextField(blank=True, max_length=100)
	github_link = models.CharField(null=True, blank=True, max_length=60)
	linkedin_link = models.CharField(null=True, blank=True, max_length=60)
	facebook_link = models.CharField(null=True, blank=True, max_length=60)
	follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
	favorites = models.ManyToManyField('Post', related_name='favorited_by', blank=True)
	favorite_comments = models.ManyToManyField('Comment', related_name='favorited_comment', blank=True)

	REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

	@property
	def imageURL(self):
		""" Returns url of user profile picture """
		try:
			url = 'http://127.0.0.1:7000/static' + self.user_pic.url
		except Exception:
			url = ''
		return url

	@property
	def number_of_created_posts(self):
		""" Returns number of posts that this user created """
		return self.created_by.count()

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

	def favorite_comment(self, comment):
		""" Favorite `comment` if we haven't already favorited it"""
		self.favorite_comments.add(comment)

	def unfavorite(self, article):
		"""Unfavorite `article` if we've already favorited it."""
		self.favorites.remove(article)

	def unfavorite_comment(self, comment):
		""" Unfavorite `comment` if we've already favorited it """
		self.favorite_comments.remove(comment)

	def has_favorited(self, article):
		"""Returns True if we have favorited `article`; else False."""
		return self.favorites.filter(pk=article.pk).exists()

	def has_favorited_comment(self, comment):
		""" Returns True is we have favorited `comment`; else False"""
		return self.favorite_comments.filter(id=comment.id).exists()


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="created_by")
	title = models.CharField(max_length=100, null=False, blank=False, unique=True)
	description = models.CharField(max_length=200, null=False, blank=False, default='')
	content = models.CharField(max_length=2000, null=False, blank=False)
	image = models.ImageField(upload_to='post_pics', default='default.png', height_field=None, width_field=None, max_length=None)
	created_at = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField('Tag', related_name='posts')

	@property
	def imageURL(self):
		try:
			url = 'http://127.0.0.1:7000/static' + self.image.url
		except Exception:
			url = ''
		return url

	@property
	def favorites_count(self):
		return self.favorited_by.count()

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
	content = models.CharField(max_length=2000, null=False, blank=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)

	def __str__(self):
		return f'{self.author.username} on {self.post}'


class Tag(models.Model):
	tag = models.CharField(max_length=255)

	def __str__(self):
		return self.tag
