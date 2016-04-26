from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r"^l(?P<line_pk>\d+)/p(?P<step_pk>\d+)/modifications/add/$",    views.DetailStoryVariants.as_view(),                    name="story_detail_line_part_modification_add"),
    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/modifications/$",        views.DetailStoryVariants.as_view(),                    name="story_detail_line_part_modifications"),

    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/add/$",                  views.CreateStoryPart.as_view(view_mode="next_step"),   name="story_detail_line_part_add"),
    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/$",                      views.DetailStory.as_view(),                            name="story_detail_line_part"),

    url(r"^l(?P<line_pk>\d+)/$",                                        views.DetailStory.as_view(),                            name="story_detail_line"),

    url(r"^s(?P<story_pk>\d+)/edit/$",                                  views.EditStory.as_view(),                              name="story_edit"),
    url(r"^s(?P<story_pk>\d+)/$",                                       views.DetailStory.as_view(),                            name="story_detail"),

    url(r"^list/$",                                                     views.ListStories.as_view(),                            name="story_list"),
    url(r"^add/$",                                                      views.CreateStory.as_view(),                            name="story_create"),

    url(r"^$",                                                          TemplateView.as_view(template_name="story/index.html"), name="story_index"),
]