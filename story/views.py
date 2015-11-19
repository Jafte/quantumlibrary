import random
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from story.models import Story, StoryPart
from vanilla import ListView, DetailView, FormView

from .forms import StoryForm

class ListStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False)

class DetailStory(DetailView):
    model = Story

    def get_context_data(self, **kwargs):
        context = super(DetailStory, self).get_context_data(**kwargs)
        context['story_parts'] = []
        story = self.get_object()
        
        part_pk = self.kwargs.get('step', False)
        if part_pk:
            part = get_object_or_404(StoryPart.objects.filter(story=story), pk=part_pk)
        else:
            if story.primary_story_line:
                part = story.primary_story_line
            else:
                raise Http404

        context['story_parts'] = part.get_ancestors(include_self=True)

        return context

class CreateStory(FormView):
    form_class = StoryForm
    template_name = 'story/story_form.html'
    
    def form_valid(self, form):
        story = Story(
                title = form.cleaned_data['title'],
                anotation = form.cleaned_data['anotation'],
            )

        part = StoryPart(
                text = form.cleaned_data['text'],
            )

        if self.request.user.is_authenticated():
            story.creator = self.request.user
            part.author = self.request.user
        else:
            anon_id = self.request.session.get('anon_id', False)
            if not anon_id:
                anon_id = hex(random.getrandbits(128))[2:-1]
                self.request.session['anon_id'] = anon_id

            story.session_key = anon_id
            part.session_key = anon_id
        
        story.save()
        for tag in form.cleaned_data['tags']:
            story.tags.add(tag)
        
        
        part.story = story
        part.save()
    
        story.primary_story_line = part
        story.save()
        
        return HttpResponseRedirect(story.get_absolute_url())

class EditStory(FormView):
    form_class = StoryForm
    template_name = 'story/story_form.html'
