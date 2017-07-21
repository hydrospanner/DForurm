"""
Definition of forms.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from forum.models import Topic, Post, Forum


class PostForm(forms.ModelForm):    
    class Meta():
        model = Post
        exclude = ('creator', 'updated', 'created', 'topic', 'user_ip',)


class TopicForm(forms.ModelForm):    
    title = forms.CharField(max_length=60, required=True)

    class Meta():
        model = Topic
        exclude = ('creator', 'updated', 'created', 'forum', 'user_ip', 'closed', )

class ForumForm(forms.ModelForm):    
    class Meta():
        model = Forum
        exclude = ('creator', 'updated', 'created', )