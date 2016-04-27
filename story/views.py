import random, diff_match_patch
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from vanilla import ListView, DetailView, FormView
from app.utils import JSONResponseMixin

from .forms import StoryForm, StoryEditForm, StoryPartForm
from .models import Story, StoryPart, TextBlock, StoryLine, StoryLinePart

class ListStories(ListView):
    model = Story
    queryset = Story.objects.filter(is_deleted=False)
    template_name = 'story/story_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListStories, self).get_context_data(**kwargs)
        return context

class CreateStory(FormView):
    form_class = StoryForm
    template_name = 'story/story_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateStory, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        story = Story(
            title = form.cleaned_data['title'],
            anotation = form.cleaned_data['anotation'],
            creator = self.request.user,
        )
        story.save()

        story_part = StoryPart(
            story = story
        )
        story_part.save()

        text_block = TextBlock(
            story_part = story_part,
            author = self.request.user,
            text = form.cleaned_data['text'],
        )
        text_block.save()

        story_line = StoryLine(
            story = story,
            is_primary = True,
        )
        story_line.save()

        story_line_part = StoryLinePart(
            story_line = story_line,
            story_part = story_part,
            text_block = text_block,
        )
        story_line_part.save()

        return HttpResponseRedirect(story_line.get_absolute_url())

class EditStory(FormView):
    form_class = StoryEditForm
    template_name = 'story/story_form.html'

    def get_story(self):
        story_pk = self.kwargs.get('story_pk', False)
        story = get_object_or_404(Story, pk=story_pk)
        return story

    def get(self, request, *args, **kwargs):
        story = self.get_story()
        data = {
            'title': story.title,
            'anotation': story.anotation
        }
        form = self.get_form(data)
        context = self.get_context_data(form=form)
        context['story'] = story
        return self.render_to_response(context)

    def form_valid(self, form):
        story = self.get_story()

        story.title = form.cleaned_data['title']
        story.anotation = form.cleaned_data['anotation']

        story.save()

        return HttpResponseRedirect(story.get_absolute_url())


class DetailStoryLine(DetailView):
    model = StoryLine
    lookup_url_kwarg = 'line_pk'
    template_name = 'story/story_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['story'] = self.object.story
        kwargs['story_line'] = self.object
        return kwargs

class DetailStory(DetailView):
    model = Story
    lookup_url_kwarg = 'story_pk'
    template_name = 'story/story_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['view'] = self
        kwargs['story_line'] = self.object.get_primary_story_line()
        kwargs['story'] = self.object
        return kwargs

class DetailStoryLineVariants(JSONResponseMixin, DetailView):
    model = StoryLine
    lookup_url_kwarg = 'line_pk'
    template_name = 'story/story_part_variants.html'

    def get_context_data(self, **kwargs):
        context = super(DetailStoryLineVariants, self).get_context_data(**kwargs)
        story = self.object.story

        part_pk = self.kwargs.get('part_pk', False)
        if part_pk:
            story_line_part = get_object_or_404(StoryLinePart, pk = part_pk)
        else:
            raise Http404

        context['part_original'] = story_line_part
        context['part_variants'] = story_line_part.get_all_lines_part()
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            original_story = context['part_original']
            part_variants = context['part_variants']
            parts = []
            for part in part_variants:
                data = {
                     "id": part.pk,
                     "url": [],
                     "text": part.text_block.text
                }

                reverse("story_detail_line_part", kwargs={"story_pk": context['story_line'].pk, "part_pk": part.pk})
                parts.append()
            return self.render_to_json_response({
                "part_original": {
                    "id": original_story.pk
                },
                "part_variants": parts
            })
        else:
            return super(DetailStoryLineVariants, self).render_to_response(context)


class CreateStoryPart(FormView):
    form_class = StoryPartForm
    template_name = 'story/story_form.html'
    view_mode = 'variant'

    def get_context_data(self, **kwargs):
        context = super(CreateStoryPart, self).get_context_data(**kwargs)

        part_pk = self.kwargs.get('step_pk', False)
        line_pk = self.kwargs.get('line_pk', False)

        story = get_object_or_404(Story, pk = story_pk)
        part = get_object_or_404(StoryPart.objects.filter(story=story), pk = part_pk)

        if self.view_mode == 'variant' or self.view_mode == 'modify':
            context['current_part'] = part
            context['parent_part'] = part.parent
        else:
            context['current_part'] = False
            context['parent_part'] = part

        context['view_mode'] = self.view_mode
        context['story'] = story

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        story = context['story']
        parent_part = context['parent_part']
        current_part = context['current_part']

        if self.view_mode == "modify":
            diff_obj = diff_match_patch.diff_match_patch()

            text_block = current_part.text_block

            text_block_version = TextBlockVersion(
                text = form.cleaned_data['text'],
                text_block = text_block
            )

            if self.request.user.is_authenticated():
                text_block_version.author = self.request.user
            else:
                anon_id = self.request.session.get('anon_id', False)
                if not anon_id:
                    anon_id = hex(random.getrandbits(128))[2:-1]
                    self.request.session['anon_id'] = anon_id

                text_block_version.session_key = anon_id

            diffs = diff_obj.diff_main(text_block.text, text_block_version.text)
            diff_obj.diff_cleanupSemantic(diffs)
            text_block_version.diff = diff_obj.diff_toDelta(diffs)

            text_block_version.save()

            part = current_part

        else:
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
            part.text_block = text_block
            part.save()

            parent_part.update_primary_story_line(part)

            if (parent_part == story.primary_story_line):
                story.primary_story_line = part
                story.save()

        return HttpResponseRedirect(part.get_absolute_url())
