"""
Customizations for the Django administration interface.
"""

from django.contrib import admin
# from app.models import Choice, Poll

from forum.models import Forum, Topic, Post

#class ChoiceInline(admin.TabularInline):
#    """Choice objects can be edited inline in the Poll editor."""
#    model = Choice
#    extra = 3


class ForumAdmin(admin.ModelAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "topic", "creator", "created"]

admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)