from django.forms import ModelForm, CheckboxSelectMultiple, DateInput, RadioSelect, TextInput
from django import forms

from .models import Document, Tag


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['status', 'subject', 'counterparty', 'tags', 'document_date', 'document_amount']
        widgets = {
            'tags': CheckboxSelectMultiple,
            'document_date': DateInput(attrs={'type': 'date'}),
            'status': RadioSelect,
            }

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'subtag', 'fill_color', 'text_color']
        widgets = {
            'name': TextInput(attrs={'size': '12'}),
            'subtag': TextInput(attrs={'size': '12'}),
            'text_color': TextInput(attrs={'type': 'color'}),
            'fill_color': TextInput(attrs={'type': 'color'}),
        }

class SearchForm(forms.Form):
    q = forms.CharField(max_length=200, required=False)
    date_from = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    date_to = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    #tags = forms.ModelMultipleChoiceField(Tag.objects, widget=CheckboxSelectMultiple, required=False)
    tags = forms.ModelChoiceField(Tag.objects, required=False)
