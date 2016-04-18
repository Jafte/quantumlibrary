from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r"^s(?P<story_pk>\d+)/b(?P<step_pk>\d+)/variants/add/$", views.CreateStoryPart.as_view(view_mode="variant"), name="story_part_create_variant"),
    url(r"^s(?P<story_pk>\d+)/b(?P<step_pk>\d+)/variants/$", views.DetailStoryVariants.as_view(), name="story_detail_part_variants"),
    url(r"^s(?P<story_pk>\d+)/b(?P<step_pk>\d+)/next/$", views.CreateStoryPart.as_view(view_mode="next_step"), name="story_part_create_next"),
    url(r"^s(?P<story_pk>\d+)/b(?P<step_pk>\d+)/$", views.DetailStory.as_view(), name="story_detail_by_part"),
    url(r"^s(?P<story_pk>\d+)/edit/$", views.EditStory.as_view(), name="story_edit"),
    url(r"^s(?P<story_pk>\d+)/tree/$", views.DetailStory.as_view(template_name = "story/story_tree.html"), name="story_detail_tree"),
    url(r"^s(?P<story_pk>\d+)/$", views.DetailStory.as_view(), name="story_detail"),
    url(r"^write/$", views.ListStories.as_view(), name="story_list"),
    url(r"^raed/$", views.ListFinishedStories.as_view(), name="story_reading_list"),
    url(r"^add/$", views.CreateStory.as_view(), name="story_create"),
    url(r"^$", TemplateView.as_view(template_name="story/index.html"), name="story_index"),
]