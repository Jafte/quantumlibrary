import random
from story.models import Story, StoryPart
from django.views.generic import TemplateView

class AppIndex(TemplateView):
    template_name="index.html"
    
    def get_context_data(self, **kwargs):
        context = super(AppIndex, self).get_context_data(**kwargs)
        return context

class UserProfile(TemplateView):
    template_name="profile/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        return context
