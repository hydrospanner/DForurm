"""
Definition of views.
"""

# from app.models import Choice, Poll
from forum.models import Forum
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
# hi


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
    """Renders the home page, with a list of all polls."""
    model = Forum

    def get_context_data(self, **kwargs):
        context = super(ForumListView, self).get_context_data(**kwargs)
        context['title'] = 'Forums'
        context['year'] = datetime.now().year
        return context

