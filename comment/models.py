from django.db import models
from post.models import Post
from like.models import Like

# Create your models here.
class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name = 'comments', on_delete = models.CASCADE)
    post = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.owner} ==> {self.post}'