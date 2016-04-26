from django.contrib import admin
from .models import Story, StoryPart, TextBlock, StoryLine, StoryLinePart

admin.site.register(Story)
admin.site.register(StoryPart)
admin.site.register(TextBlock)
admin.site.register(StoryLine)
admin.site.register(StoryLinePart)
