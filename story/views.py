import random
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from story.models import Story, StoryPart
from vanilla import CreateView, DeleteView, ListView, UpdateView, DetailView, \
                    FormView

from .forms import StoryForm

class ListStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False)

class DetailStory(DetailView):
    model = Story

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

class EditStory(UpdateView):
    model = Story
    success_url = reverse_lazy('story_detail')


class DeleteStory(DeleteView):
    model = Story
    success_url = reverse_lazy('story_list')