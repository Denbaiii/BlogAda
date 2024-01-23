from django.db import models
from post.models import Post

# My models here.
class Like(models.Model):
    post = models.ForeignKey(Post, related_name = 'likes', on_delete = models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name = 'likes', on_delete = models.CASCADE)

class Favorite(models.Model):
    post = models.ForeignKey(Post, related_name = 'favorites', on_delete = models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name = 'favorites', on_delete = models.CASCADE)
