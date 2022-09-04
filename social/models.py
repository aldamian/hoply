from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


def make_id():

    return int(uuid.uuid4().hex[:8], 16)
    

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.BigIntegerField(default=make_id)
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField() # naming this as content will duplicate this field in PostForm
    
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    hates = models.ManyToManyField(User, related_name='hates', blank=True)
    cares = models.ManyToManyField(User, related_name='cares', blank=True)

    stamp = models.DateTimeField(auto_now_add=True)
    edited_stamp = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    created_on = models.DateTimeField(default=timezone.now)


class Reaction(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


    REACTION_CHOICES = (
        (0, 'Reaction Deleted'),
        (1, 'Like'),
        (2, 'Hate'),
        (3, 'Couldn\'t Care Less'),
    )

    choice = models.IntegerField(choices=REACTION_CHOICES)

    stamp = models.DateTimeField(auto_now=True)