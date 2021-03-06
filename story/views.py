import diff_match_patch
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.html import linebreaks

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditStory, self).dispatch(*args, **kwargs)

    def get_story(self):
        story_pk = self.kwargs.get('story_pk', False)
        story = get_object_or_404(Story, pk=story_pk)

        if story.creator != self.request.user:
            raise Http404

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
        story_line = self.object

        part_pk = self.kwargs.get('part_pk', False)
        if part_pk:
            story_line_part = get_object_or_404(StoryLinePart, pk=part_pk)
        else:
            raise Http404

        if story_line_part.story_line != story_line:
            raise Http404

        context['story_line_part'] = story_line_part
        context['part_variants'] = story_line_part.get_all_lines_part()
        context['story'] = story_line.story
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            story_line_part = context['story_line_part']
            part_variants = context['part_variants']
            parts = []
            for part in part_variants:
                data = {
                    "id": part.pk,
                    "url": reverse("story_detail_line", kwargs={"line_pk": part.story_line.pk}),
                    "text": linebreaks(part.text_block.text)
                }
                parts.append(data)
            return self.render_to_json_response({
                "part_original": {
                    "id": story_line_part.pk
                },
                "part_variants": parts
            })
        else:
            return super(DetailStoryLineVariants, self).render_to_response(context)

class DetailStoryLineModifications(JSONResponseMixin, DetailView):
    model = StoryLine
    lookup_url_kwarg = 'line_pk'
    template_name = 'story/story_part_modifications.html'

    def get_context_data(self, **kwargs):
        context = super(DetailStoryLineModifications, self).get_context_data(**kwargs)
        story_line = self.object

        part_pk = self.kwargs.get('part_pk', False)
        if part_pk:
            story_line_part = get_object_or_404(StoryLinePart, pk = part_pk)
        else:
            raise Http404

        if story_line_part.story_line != story_line:
            raise Http404

        context['story_line_part'] = story_line_part
        context['part_variants'] = story_line_part.get_all_text_block_variants()
        context['story'] = story_line.story
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            story_line_part = context['story_line_part']
            part_variants = context['part_variants']
            parts = []
            for part in part_variants:
                data = {
                     "id": part.pk,
                     "url": reverse("story_detail_line", kwargs={"line_pk": part.story_line.pk}),
                     "text": linebreaks(part.text_block.text)
                }
                parts.append(data)
            return self.render_to_json_response({
                "part_original": {
                    "id": story_line_part.pk
                },
                "part_variants": parts
            })
        else:
            return super(DetailStoryLineModifications, self).render_to_response(context)


class CreateStoryPart(FormView):
    form_class = StoryPartForm
    template_name = 'story/story_form.html'
    view_mode = 'mod'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateStoryPart, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateStoryPart, self).get_context_data(**kwargs)

        part_pk = self.kwargs.get('part_pk', False)
        line_pk = self.kwargs.get('line_pk', False)

        story_line = get_object_or_404(StoryLine, pk = line_pk)
        story = story_line.story
        story_line_part = get_object_or_404(StoryLinePart, pk = part_pk)

        if story_line_part.story_line.story != story:
            raise Http404

        context['view_mode'] = self.view_mode
        context['story_line_part'] = story_line_part
        context['story'] = story

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        story = context['story']
        story_line_part = context['story_line_part']
        view_mode = context['view_mode']

        if view_mode == "mod":
            diff_obj = diff_match_patch.diff_match_patch()

            text_block_original = story_line_part.text_block

            text_block = TextBlock(
                text=form.cleaned_data['text'],
                parent=text_block_original,
                author=self.request.user,
                story_part=story_line_part.story_part,
            )

            diffs = diff_obj.diff_main(text_block_original.text, text_block.text)
            diff_obj.diff_cleanupSemantic(diffs)

            text_block.diff = diff_obj.diff_toDelta(diffs)

            text_block.save()

            original_story_line = story_line_part.story_line
            story_line = StoryLine(story=story)
            story_line.save()

            for part in original_story_line.parts.all():
                part.pk = None
                part.parent = None
                part.story_line = story_line

                if part.story_part == story_line_part.story_part:
                    part.text_block = text_block
                    part.parent = story_line_part.parent if  story_line_part.parent  else story_line_part

                part.save()

        else:
            if view_mode == "next":
                parent = story_line_part.story_part
            else:
                parent = story_line_part.story_part.parent

            original_story_line = story_line_part.story_line
            last_part = original_story_line.get_last_part()

            story_part = StoryPart(
                    parent = parent,
                    story = story
                )
            story_part.save()

            text_block = TextBlock(
                text=form.cleaned_data['text'],
                author = self.request.user,
                story_part = story_part,
            )

            text_block.save()

            if last_part.story_part == parent:
                new_part = StoryLinePart(
                            story_line = original_story_line,
                            story_part = story_part,
                            text_block = text_block
                        )
                new_part.save()
                story_line = original_story_line
            else:
                story_line = StoryLine(story=story)
                story_line.save()

                for part_line in story_line.parts.all():
                    part_line.pk = None
                    part_line.parent = None
                    part_line.story_line = story_line

                    if part_line.story_part == parent:
                        part_line.text_block = text_block
                        part_line.story_part = story_part

                    part_line.save()

                    if part_line.story_part == parent:
                        break

        return HttpResponseRedirect(story_line.get_absolute_url())
