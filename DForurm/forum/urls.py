"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import url
#from app.models import Poll

import forum.views

urlpatterns = [
    url(r'^$', forum.views.test_index, name='index'),

]
