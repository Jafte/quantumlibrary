from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/modifications/add/$",    views.CreateStoryPart.as_view(view_mode="mod"), name="story_detail_line_part_modification_add"),
    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/modifications/$",        views.DetailStoryLineModifications.as_view(),                name="story_detail_line_part_modifications"),

    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/variants/add/$",         views.CreateStoryPart.as_view(view_mode="variant"),     name="story_detail_line_part_variant_add"),
    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/variants/$",             views.DetailStoryLineVariants.as_view(),                name="story_detail_line_part_variants"),

    url(r"^l(?P<line_pk>\d+)/p(?P<part_pk>\d+)/next/$",                 views.CreateStoryPart.as_view(view_mode="next"),        name="story_detail_line_part_next"),
    url(r"^l(?P<line_pk>\d+)/$",                                        views.DetailStoryLine.as_view(),                        name="story_detail_line"),

    url(r"^s(?P<story_pk>\d+)/edit/$",                                  views.EditStory.as_view(),                              name="story_edit"),
    url(r"^s(?P<story_pk>\d+)/$",                                       views.DetailStory.as_view(),                            name="story_detail"),

    url(r"^list/$",                                                     views.ListStories.as_view(),                            name="story_list"),
    url(r"^add/$",                                                      views.CreateStory.as_view(),                            name="story_create"),

    url(r"^$",                                                          TemplateView.as_view(template_name="story/index.html"), name="story_index"),
]