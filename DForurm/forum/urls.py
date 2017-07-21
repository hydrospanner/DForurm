"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import url
from forum.models import Forum

import forum.views

urlpatterns = [
    url(r'^$',
        forum.views.ForumListView.as_view(
            queryset=Forum.objects.order_by('-updated')[:10],
            context_object_name='latest_forum_list',
            template_name='forum/index.html',),
        name='forum-home'),
    url(r'^f/(?P<slug>[-\w]+)/$',
        forum.views.ForumDetailView.as_view(
            template_name='forum/forum-details.html'),
        name='forum-detail'),
    url(r'^(?P<pk>\d+)/$',
        forum.views.TopicDetailView.as_view(
            template_name='forum/topic-details.html'),
        name='topic-detail'),
    url(r'^reply/(\d+)/$', forum.views.post_reply, name='reply'),
    url(r'^newtopic/(?P<slug>[-\w]+)/$', forum.views.new_topic, name='new-topic'),
    url(r'^newforum/$', forum.views.new_forum, name='new-forum'),

]

'''
url(r'^(?P<pk>\d+)/$',
    forum.views.ForumDetailView.as_view(
        template_name='forum/forum-details.html'),
    name='forum-detail'),
'''
    # url(r'^$', forum.views.test_index, name='index'),
