import random
from story.models import Story
from django.views.generic import TemplateView

class AppIndex(TemplateView):
    template_name = "story/story_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(AppIndex, self).get_context_data(**kwargs)
        context["story_list"] = Story.objects.filter(is_deleted=False, is_finished=False)[:15]
        return context

class UserProfile(TemplateView):
    template_name = "profile/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        return context
