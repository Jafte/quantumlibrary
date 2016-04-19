from django.utils.translation import ugettext_lazy as _
from django import forms

class StoryForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=200)
    anotation = forms.CharField(label=_('Description'), required=False, widget=forms.Textarea(attrs={'rows':5, 'cols':40}))
    text = forms.CharField(label=_('First part'), widget=forms.Textarea(attrs={'rows':10, 'cols':40}))

class StoryPartForm(forms.Form):
    text = forms.CharField(label=_('Text'), widget=forms.Textarea(attrs={'rows':15, 'cols':40}))
    variant = forms.BooleanField(label=_('Variant'), widget=forms.CheckboxInput(), help_text=_("Save the narrative line (all subsequent episodes will be transferred)"))