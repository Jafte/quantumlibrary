from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Story, StoryPart, TextBlock, TextBlockVersion

admin.site.register(Story)
admin.site.register(TextBlock)
admin.site.register(TextBlockVersion)
admin.site.register(StoryPart, MPTTModelAdmin)