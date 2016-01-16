from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.ListStories.as_view(), name="story_list"),
    url(r"^raed/$", views.ListFinishedStories.as_view(), name="story_reading_list"),
    url(r"^add/$", views.CreateStory.as_view(), name="story_create"),
    url(r"^s(?P<story_pk>\d+)/$", views.DetailStory.as_view(), name="story_detail"),
    url(r"^s(?P<story_pk>\d+)/tree/$", views.DetailStory.as_view(template_name = "story/story_tree.html"), name="story_detail_tree"),
    url(r"^s(?P<story_pk>\d+)/d(?P<step_pk>\d+)/$", views.DetailStory.as_view(), name="story_detail_by_part"),
    url(r"^s(?P<story_pk>\d+)/d(?P<step_pk>\d+)/add/$", views.CreateStoryPart.as_view(), name="story_part_create"),
    url(r"^s(?P<story_pk>\d+)/edit/$", views.EditStory.as_view(), name="story_edit"),
]