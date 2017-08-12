"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import url
import forum.views

urlpatterns = [
    url(r'^$', forum.views.IndexView, name='forum-home'),
    url(r'^f/(?P<slug>[-\w]+)/$', forum.views.forum_topics, name='forum-detail'),
    url(r'^(?P<pk>\d+)/$', forum.views.topic_posts, name='topic-detail'),
    url(r'^reply/(\d+)/$', forum.views.post_reply, name='reply'),
    url(r'^newtopic/(?P<slug>[-\w]+)/$', forum.views.new_topic, name='new-topic'),
    url(r'^newforum/$', forum.views.new_forum, name='new-forum'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', forum.views.user_posts, name='user-posts'),
    url(r'^user/topics/(?P<username>[\w.@+-]+)/$', forum.views.user_topics, name='user-topics'),
]
