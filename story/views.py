import random
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from story.models import Story, StoryPart
from vanilla import ListView, DetailView, FormView
from taggit.utils import edit_string_for_tags

from .forms import StoryForm, StoryPartForm

class ListStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False).exclude(primary_story_line__isnull=True)

class ListFinishedStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False, is_finished=True).exclude(primary_story_line__isnull=True)

class DetailStory(DetailView):
    model = Story
    lookup_url_kwarg = 'story_pk'

    def get_context_data(self, **kwargs):
        context = super(DetailStory, self).get_context_data(**kwargs)
        context['story_parts'] = []
        story = self.object
        
        part_pk = self.kwargs.get('step_pk', False)
        root_part = get_object_or_404(StoryPart.objects.filter(story=story), level=0)
        if part_pk:
            part = get_object_or_404(StoryPart.objects.filter(story=story), pk=part_pk)
            if part.primary_story_line:
                part = part.primary_story_line
        else:
            if story.primary_story_line:
                part = story.primary_story_line
            else:
                raise Http404

        context['primary_story_line'] = part
        context['root_story_line'] = root_part
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

class CreateStoryPart(FormView):
    form_class = StoryPartForm
    template_name = 'story/story_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(CreateStoryPart, self).get_context_data(**kwargs)
        
        parent_part_pk = self.kwargs.get('step_pk', False)
        story_pk = self.kwargs.get('story_pk', False)
        
        story = get_object_or_404(Story, pk=story_pk)
        parent_part = get_object_or_404(StoryPart.objects.filter(story=story), pk=parent_part_pk)
        
        context['story'] = story
        context['parent_part'] = parent_part
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        story = context['story']
        parent_part = context['parent_part']
        
        part = StoryPart(
                parent = parent_part,
                text = form.cleaned_data['text'],
            )

        if self.request.user.is_authenticated():
            part.author = self.request.user
        else:
            anon_id = self.request.session.get('anon_id', False)
            if not anon_id:
                anon_id = hex(random.getrandbits(128))[2:-1]
                self.request.session['anon_id'] = anon_id

            part.session_key = anon_id
        
        part.story = story
        part.save()

        parent_part.update_primary_story_line(part)

    
        if (parent_part == story.primary_story_line):
            story.primary_story_line = part
            story.save()
        
        return HttpResponseRedirect(part.get_absolute_url())


class EditStory(FormView):
    form_class = StoryForm
    template_name = 'story/story_form.html'

    def get_story(self):
        story_pk = self.kwargs.get('story_pk', False)
        story = get_object_or_404(Story, pk=story_pk)
        return story

    def get(self, request, *args, **kwargs):
        story = self.get_story()
        data = {
            'title': story.title,
            'anotation': story.anotation,
            'tags': edit_string_for_tags([o for o in story.tags.all()]),
            'text': story.get_first_part().text
        }
        form = self.get_form(data)
        context = self.get_context_data(form=form)
        context['story'] = story
        return self.render_to_response(context)
