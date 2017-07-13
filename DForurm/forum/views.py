"""
Definition of views.
"""

# from app.models import Choice, Poll
from forum.models import Forum, Topic
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
from os import path

# import json


def test_index(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'forum/index.html',
        {
        }
    )

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