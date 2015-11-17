from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.ListStories.as_view(), name="story_list"),
    url(r"^add/$", views.CreateStory.as_view(), name="story_create"),
    url(r"^s(?P<pk>\w+)/$", views.DeleteStory, name="story_detail"),
    url(r"^s(?P<pk>\w+)/edit/$", views.EditStory, name="story_edit"),
]