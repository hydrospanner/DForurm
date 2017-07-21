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
from forum.forms import PostForm, TopicForm, ForumForm

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

    def get_queryset(self):
        # not working...
        return Topic.objects.order_by("-created")

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

@login_required
def new_topic(request, slug):
    form = TopicForm()
    forum = get_object_or_404(Forum, slug=slug)
    
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():

            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.forum = forum
            topic.creator = request.user

            topic.save()

            return HttpResponseRedirect(reverse('forum:forum-detail', args=(forum.slug, )))

    context = {'form': form, 'forum': forum}
    return render(request, 'forum/new-topic.html', context)

@login_required
def new_forum(request):
    form = ForumForm()
    # forum = get_object_or_404(Forum, slug=slug)
    
    if request.method == 'POST':
        form = ForumForm(request.POST)

        if form.is_valid():

            forum = Forum()
            forum.slug = form.cleaned_data['slug']
            forum.description = form.cleaned_data['description']
            forum.creator = request.user

            forum.save()

            return HttpResponseRedirect(reverse('forum:forum-home', ))

    context = {'form': form}
    return render(request, 'forum/new-forum.html', context)

'''
@login_required
def seed(request):
    """Seeds the database with sample polls."""
    samples_path = path.join(path.dirname(__file__), 'samples.json')
    with open(samples_path, 'r') as samples_file:
        samples_polls = json.load(samples_file)

    for sample_poll in samples_polls:
        poll = Poll()
        poll.text = sample_poll['text']
        poll.pub_date = timezone.now()
        poll.save()

        for sample_choice in sample_poll['choices']:
            choice = Choice()
            choice.poll = poll
            choice.text = sample_choice
            choice.votes = 0
            choice.save()

    return HttpResponseRedirect(reverse('app:home'))
'''