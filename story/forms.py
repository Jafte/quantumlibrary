from django.utils.translation import ugettext_lazy as _
from django import forms

class StoryForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=200)
    anotation = forms.CharField(label=_('Description'), required=False, widget=forms.Textarea())
    text = forms.CharField(label=_('First part'), widget=forms.Textarea())

class StoryPartForm(forms.Form):
    text = forms.CharField(label=_('Text'), widget=forms.Textarea())