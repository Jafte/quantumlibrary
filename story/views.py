import random
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from story.models import Story
from vanilla import CreateView, DeleteView, ListView, UpdateView

class ListStories(ListView):
    model = Story


class CreateStory(CreateView):
    model = Story
    fields = ['title', 'anotation', 'tags',]

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.creator = self.request.user
        else:
            anon_id = self.request.session.get('anon_id', False)
            if not anon_id:
                anon_id = hex(random.getrandbits(128))[2:-1]
                self.request.session['anon_id'] = anon_id
            form.instance.session_key = anon_id
        self.object = form.save()
        return HttpResponseRedirect(reverse_lazy('story_detail', ))

class EditStory(UpdateView):
    model = Story
    success_url = reverse_lazy('story_detail')


class DeleteStory(DeleteView):
    model = Story
    success_url = reverse_lazy('story_list')