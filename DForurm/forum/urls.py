"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import url
#from app.models import Poll
from forum.models import Forum

import forum.views

urlpatterns = [
    # url(r'^$', forum.views.test_index, name='index'),
    url(r'^$',
        forum.views.ForumListView.as_view(
            queryset=Forum.objects.order_by('-updated')[:5],
            context_object_name='latest_forum_list',
            template_name='forum/index.html',),
        name='forum-home'),
    url(r'^(?P<pk>\d+)/$',
        forum.views.ForumDetailView.as_view(
            template_name='forum/forum-details.html'),
        name='forum-detail'),

]
