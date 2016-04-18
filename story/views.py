import random
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from story.models import Story, StoryPart, TextBlock
from vanilla import ListView, DetailView, FormView
from app.utils import JSONResponseMixin
from .forms import StoryForm, StoryPartForm

class ListStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False).exclude(primary_story_line__isnull=True)
    template_name = 'story/story_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ListStories, self).get_context_data(**kwargs)
        context['breadcrumbs_active_title'] = u"Пишем"
        return context
        
class ListFinishedStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False, is_finished=True).exclude(primary_story_line__isnull=True)
    template_name = 'story/story_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListFinishedStories, self).get_context_data(**kwargs)
        context['breadcrumbs_active_title'] = u"Читаем"
        return context

class DetailStory(DetailView):
    model = Story
    lookup_url_kwarg = 'story_pk'
    template_name = 'story/story_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailStory, self).get_context_data(**kwargs)
        context['story_parts'] = []
        story = self.object
        
        part_pk = self.kwargs.get('step_pk', False)
        root_part = get_object_or_404(StoryPart.objects.filter(story=story), level = 0)
        if part_pk:
            part = get_object_or_404(StoryPart.objects.filter(story=story), pk = part_pk)
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

class DetailStoryVariants(JSONResponseMixin, DetailView):
    model = Story
    lookup_url_kwarg = 'story_pk'
    template_name = 'story/story_part_variants.html'

    def get_context_data(self, **kwargs):
        context = super(DetailStoryVariants, self).get_context_data(**kwargs)
        story = self.object

        part_pk = self.kwargs.get('step_pk', False)
        if part_pk:
            part = get_object_or_404(StoryPart.objects.filter(story=story), pk = part_pk)
        else:
            raise Http404

        context['part_original'] = part
        context['part_variants'] = part.get_siblings(include_self=True)
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            original_story = context['part_original']
            part_variants = context['part_variants']
            parts = []
            for part in part_variants:
                parts.append({
                    "id": part.pk,
                    "url": reverse("story_detail_by_part", kwargs={"story_pk": context['story'].pk, "step_pk": part.pk}),
                    "text": part.text
                })
            return self.render_to_json_response({
                "part_original": {
                    "id": original_story.pk
                },
                "part_variants": parts
            })
        else:
            return super(DetailStoryVariants, self).render_to_response(context)


class CreateStory(FormView):
    form_class = StoryForm
    template_name = 'story/story_form.html'
    
    def form_valid(self, form):
        story = Story(
                title = form.cleaned_data['title'],
                anotation = form.cleaned_data['anotation'],
            )

        text_block = TextBlock(
            text = form.cleaned_data['text'],
        )
        part = StoryPart()

        if self.request.user.is_authenticated():
            story.creator = self.request.user
            text_block.author = self.request.user
        else:
            anon_id = self.request.session.get('anon_id', False)
            if not anon_id:
                anon_id = hex(random.getrandbits(128))[2:-1]
                self.request.session['anon_id'] = anon_id

            story.session_key = anon_id
            text_block.session_key = anon_id
        
        story.save()
        
        text_block.story = story
        text_block.save()
        
        part.story = story
        part.text = text_block
        part.save()
    
        story.primary_story_line = part
        story.save()
        
        return HttpResponseRedirect(story.get_absolute_url())

class CreateStoryPart(FormView):
    form_class = StoryPartForm
    template_name = 'story/story_form.html'
    view_mode = 'variant'
    
    def get_context_data(self, **kwargs):
        context = super(CreateStoryPart, self).get_context_data(**kwargs)
        
        part_pk = self.kwargs.get('step_pk', False)
        story_pk = self.kwargs.get('story_pk', False)
        
        story = get_object_or_404(Story, pk = story_pk)
        part = get_object_or_404(StoryPart.objects.filter(story=story), pk = part_pk)
        
        if self.view_mode == 'variant':
            context['current_part'] = part
            context['parent_part'] = part.parent
        else:
            context['current_part'] = False
            context['parent_part'] = part
            
        context['story'] = story

        return context
    
    def form_valid(self, form):
        context = self.get_context_data(form=form)
        story = context['story']
        parent_part = context['parent_part']

        text_block = TextBlock(
            text=form.cleaned_data['text'],
        )
        
        part = StoryPart(
                parent = parent_part,
            )

        if self.request.user.is_authenticated():
            text_block.author = self.request.user
        else:
            anon_id = self.request.session.get('anon_id', False)
            if not anon_id:
                anon_id = hex(random.getrandbits(128))[2:-1]
                self.request.session['anon_id'] = anon_id

            text_block.session_key = anon_id
        
        text_block.story = story
        text_block.save()

        part.story = story
        part.text = text_block
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
            'text': story.get_first_part().text
        }
        form = self.get_form(data)
        context = self.get_context_data(form=form)
        context['story'] = story
        return self.render_to_response(context)
