from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from story.models import Story, StoryPart

admin.site.register(Story)
admin.site.register(StoryPart, MPTTModelAdmin)