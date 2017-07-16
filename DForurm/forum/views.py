"""
Definition of views.
"""

from forum.models import Forum, Topic, Post
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
from os import path
from forum.forms import PostForm

# import json



class ForumListView(ListView):
    """Renders the home page, with a list of forums."""
    model = Forum

    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['title'] = 'Forums'
        context['year'] = datetime.now().year
        context['topics'] = Topic.objects.all().order_by("-created")
        return context

class ForumDetailView(DetailView):
    """Renders the Forum details (topic list) page."""
    model = Forum

    def get_context_data(self, **kwargs):
        context = super(ForumDetailView, self).get_context_data(**kwargs)
        context['title'] = 'forum'
        context['year'] = datetime.now().year
        return context

class TopicDetailView(DetailView):
    """Renders the Forum details (topic list) page."""
    model = Topic

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Topic -- this is not being used'
        context['year'] = datetime.now().year
        # pass in the forum too, so the topic template can borrow from the forum template
        # context['forum'] = context['Topic'].forum # this isn't working
        return context


@login_required
def post_reply(request, topic_id):
    form = PostForm()
    topic = Topic.objects.get(pk=topic_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():

            post = Post()
            post.topic = topic
            post.body = form.cleaned_data['body']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']

            post.save()

            return HttpResponseRedirect(reverse('forum:topic-detail', args=(topic.id, )))

    context = {'form': form, 'topic': topic}
    return render(request, 'forum/reply.html', context)
