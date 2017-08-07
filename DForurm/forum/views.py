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

def get_base_context():
    return {'year': datetime.now().year}

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
    context = get_base_context()
    context['forums'] = Forum.objects.all()[:20]
    topics = Topic.objects.all().order_by('-created')
    context['topics'] = paginator_helper(request, topics)
    context['title'] = 'Welcome'
    return render(request, 'forum/index.html', context)

def forum_topics(request, slug):
    context = get_base_context()
    context['forum'] = Forum.objects.get(slug=slug)
    topics = Topic.objects.filter(forum__slug=slug).order_by('-created')
    context['topics'] = paginator_helper(request, topics)
    context['title'] = context['forum'].slug
    return render(request, 'forum/forum-details.html', context)

def topic_posts(request, pk):
    context = get_base_context()
    posts = Post.objects.filter(topic__pk=pk).order_by('created')
    context['topic'] = Topic.objects.get(pk=pk)
    context['forum'] = context['topic'].forum
    context['posts'] = paginator_helper(request, posts)
    context['title'] = context['topic'].title + ' - ' + context['forum'].slug
    return render(request, 'forum/topic-details.html', context)

def user_posts(request, username):
    context = get_base_context()
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creator=user).order_by('-created')
    posts = paginator_helper(request, posts)
    context.update({'posts': posts, 'user': user})
    context['title'] = user.username
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
