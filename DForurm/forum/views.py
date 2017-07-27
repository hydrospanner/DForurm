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
# from django.views.generic import ListView, DetailView
from os import path
from forum.forms import PostForm, TopicForm, ForumForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# import json

def paginator_helper(request, model_list, page_items=25):
    paginator = Paginator(model_list, page_items)

    page = request.GET.get('page')
    try:
        model_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        model_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        model_list = paginator.page(paginator.num_pages)
    return model_list

def IndexView(request):
    forums = Forum.objects.all()
    topics = Topic.objects.all().order_by('-created')
    topics = paginator_helper(request, topics, 25)
    return render(request, 'forum/index.html', {'latest_forum_list': forums, 'topics': topics})

def forum_topics(request, slug):
    forum = Forum.objects.get(slug=slug)
    topics = Topic.objects.filter(forum__slug=slug).order_by('-created')
    topics = paginator_helper(request, topics, 25)
    # order_by not working...
    context = {'forum': forum, 'topics':topics}
    return render(request, 'forum/forum-details.html', context)

def topic_posts(request, pk):
    posts = Post.objects.filter(topic__pk=pk)
    topic = Topic.objects.get(pk=pk)
    forum = topic.forum
    posts = paginator_helper(request, posts, 25)
    context = {'posts': posts, 'topic': topic, 'forum': forum}
    return render(request, 'forum/topic-details.html', context)

def user_posts(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creator=user).order_by('-created')
    posts = paginator_helper(request, posts, 25)
    context = {'posts': posts, 'user': user}
    return render(request, 'forum/user-posts.html', context)

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
    """Seeds the database with sample Forums, Topics, and Posts."""
    samples_path = path.join(path.dirname(__file__), 'samples.json')
    with open(samples_path, 'r') as samples_file:
        samples_forums = json.load(samples_file)

    for sample_forum in samples_forums:
        forum = Forum()
        forum.slug= sample_forum['forum']
        forum.created = timezone.now()
        forum.save()

        for sample_topic in sample_forum['topics']:
            topic = Topic()
            topic.forum = forum
            topic.title = sample_topic['title']
            topic.save()

            for sample_post in sample_topic['posts']:
            post = Post()
            post.body = sample_post
            post.save()

    return HttpResponseRedirect(reverse('forum:forum-index'))
'''

'''
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
        return context

'''