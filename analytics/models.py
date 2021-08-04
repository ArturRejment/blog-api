from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save

from api.models import User
from .signals import object_viewed_signal
from .utils import get_client_ip


class ObjectViewed(models.Model):
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	ip_address = models.CharField(max_length=220, blank=True, null=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Post, Comment, Tag
	object_id = models.PositiveIntegerField()  # Post.id, Comment.id, Tag.id
	content_object = GenericForeignKey('content_type', 'object_id')  # Post, Comment, Tag instance
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.content_object} viewed on {self.timestamp}'

	class Meta:
		ordering = ['-timestamp']
		verbose_name = 'Object viewed'
		verbose_name_plural = 'Objects viewed'


def object_viewed_reciever(sender, instance, request, *args, **kwargs):
	c_type = ContentType.objects.get_for_model(sender)
	if request.user.is_authenticated:
		user = request.user
	else:
		user = None
	new_view_obj = ObjectViewed.objects.create(
		user=user,
		ip_address=get_client_ip(request),
		object_id = instance.id,
		content_type=c_type
	)

object_viewed_signal.connect(object_viewed_reciever)