from django.contrib import admin
from .models import Profile,Post,Comment,Message
from . import models
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(models.LikePost)
admin.site.register(models.FriendRequest)