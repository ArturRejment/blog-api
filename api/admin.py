from django.contrib import admin
from .models import Post, User, Comment, Tag


admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Tag)