from django.utils.translation import ugettext_lazy as _
from django import forms
from taggit.forms import TagField

class StoryForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=200)
    anotation = forms.CharField(label=_('Description'), required=False, widget=forms.Textarea())
    text = forms.CharField(label=_('First part'), widget=forms.Textarea())
    tags = TagField(label=_('Tags'), required=False)