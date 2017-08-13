"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Forum(models.Model):
    slug = models.SlugField(unique=True, max_length=60)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.slug

    def num_posts(self):
        return sum([t.num_posts() for t in self.topic_set.all()])


class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True)
    forum = models.ForeignKey(Forum)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)

    def num_posts(self):
        return self.post_set.count()

    def __str__(self):
        return self.creator.get_username() + " - " + self.title


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic)
    body = models.TextField(max_length=10000)
    user_ip = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return u"%s - %s" % (self.creator, self.topic)
