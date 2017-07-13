"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Forum(models.Model):
    slug = models.SlugField(unique=True, max_length=60)
    # title = slug
    # slug = title
    description= models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.slug

    def num_posts(self):
        return sum([t.num_posts() for t in self.topic_set.all()])

    def last_post(self):
        if self.topic_set.count():
            last = None
            for t in self.topic_set.all():
                l = t.last_post()
                if l:
                    if not last: last = l
                    elif l.created > last.created: last = l
            return last


class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    forum = models.ForeignKey(Forum)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return max(0, self.post_set.count() - 1)

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]

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

    def short(self):
        return u"%s\n%s" % (self.creator, self.created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True